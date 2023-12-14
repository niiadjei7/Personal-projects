from django.db import models

class Budget(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def total_expenses(self):
        return self.expense_set.aggregate(models.Sum('amount'))['amount__sum'] or 0

class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
# Create your models here.
