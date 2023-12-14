#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define MAX_WORD_LENGTH 256


struct NumWord{
	char word[MAX_WORD_LENGTH];
	int num;
	struct NumWord* next;
};

typedef struct NumWord NumWord;

#define HASH_SIZE 10000

NumWord* hashTable[HASH_SIZE];
//map word to an index on the hash table
unsigned long hash(char *word){
	unsigned long hash = 5381;//arbitrary prime number
	int c;

	while ((c = *word++)){
		hash = ((hash << 5) + hash) + c;
	}

	return (hash % HASH_SIZE);
}

void insertWord(char *word) {
    	unsigned long i = hash(word);

    	if (hashTable[i] == NULL) {
        	NumWord *new = (NumWord *)malloc(sizeof(NumWord));
        	strcpy(new->word, word);
        	new->num = 1;
        	new->next = NULL; // Ensure new node's next is set to NULL
        	hashTable[i] = new;
    	} else {
        	NumWord *w = hashTable[i];
        	while (w != NULL) {
            		if (strcmp(w->word, word) == 0) {
                		w->num++;
                		return;
            		}
            		w = w->next;
        	}

        	NumWord *new = (NumWord *)malloc(sizeof(NumWord));
        	strcpy(new->word, word);
        	new->num = 1;
        	new->next = hashTable[i];
        	hashTable[i] = new;
    	}
}


//function to determine what counts as a word
char* readWord(FILE *file) {
        int bufferSize = 10; // Initial buffer size
        char *buffer = malloc(bufferSize * sizeof(char));
        int length = 0;

        int c;
	int pendingHyphen = 0;
        while ((c = fgetc(file)) != EOF){ 
		if (isalpha(c) || c == '\''){
			if (pendingHyphen == 1){
				buffer[length++] = '_';
				pendingHyphen = 0;
			}
		       	buffer[length++] = c;
		}
		else if (c == '-' && length > 0) {
			if (pendingHyphen == 1){
				break;
			}
			else{
				pendingHyphen = 1;
			}
                }
		else{
			break;
		}

                if (length + 1 >= bufferSize) {
                        bufferSize *= 2;
                        buffer = realloc(buffer, bufferSize * sizeof(char));
                }

        }
	
	buffer[length] = '\0';

	if (c == EOF){
		return NULL;
	}

	return buffer;
}


void readFile(char *filePath) {

	FILE *file = fopen(filePath, "r");
	if (filePath == NULL){
		printf("Error: Unable to open file - %s\n", filePath);
	}
    	char *word;
    
    	while ((word = readWord(file)) != NULL) {
        	insertWord(word);
        	free(word);
    	}

	fclose(file);
}




void readDirectory(char *directoryPath){
	struct dirent *entry;
	DIR *dpath = opendir(directoryPath);

	if (dpath == NULL){
		printf("Error: Unable to open directory - %s\n", directoryPath);
		return;
	}

	while ((entry = readdir(dpath))){
		if (entry->d_type == DT_REG && strstr(entry->d_name, ".txt")) {
        		char filePath[512];
            		readFile(filePath);
        	}
		else if (entry->d_type == DT_DIR && strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
            		char subDirPath[512];
        		readDirectory(subDirPath);
        	}
	}
	closedir(dpath);
}

void printWords(int total) {
	NumWord* numWords[HASH_SIZE];
	int count = 0;

    	for (int i = 0; i < HASH_SIZE; i++) {
        	NumWord* cWord = hashTable[i];
        	while (cWord != NULL) {
            		numWords[count] = cWord;
					total++;
            		count++;
            		cWord = cWord->next;
        	}
    	}

    	for (int i = 0; i < count - 1; i++) {
        	for (int j = 0; j < count - i - 1; j++) {
            		if (numWords[j]->num < numWords[j + 1]->num) {
                		NumWord* temp = numWords[j];
                		numWords[j] = numWords[j + 1];
                		numWords[j + 1] = temp;
            		}
        	}
    	}

    	char output[MAX_WORD_LENGTH + 12];  // Max word length + space for count and newline

    	for (int i = 0; i < count; i++) {
        	sprintf(output, "%s %d\n", numWords[i]->word, numWords[i]->num);
        	write(STDOUT_FILENO, output, strlen(output));	
    	}
		printf("Total word count = %d", total);
}


int main(int argc, char *argv[]){
	int total = 0;
	if (argc < 2){
		printf("Error, No files or directories provided for input. \n");
		return 1;
	}
	for (int i = 0; i < HASH_SIZE; i++){
		hashTable[i] = NULL;
	}
	for (int i = 1; i < argc; i++){
		struct stat path_stat;
		if (stat(argv[i], &path_stat) == 0){
			if (S_ISREG(path_stat.st_mode)){
				readFile(argv[i]);
			}
			else if (S_ISDIR(path_stat.st_mode)){
				readDirectory(argv[i]);
			}
			else{
				printf("Error, Invalid argument - %s\n", argv[i]);
			}
		}
		else{
			printf("Error, Invalid argument - %s\n", argv[i]);
		}
	}

	printWords(total);

	return 0;
}
