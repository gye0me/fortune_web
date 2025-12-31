from django.db import models

class FortuneHistory(models.Model):
    # 사용자 정보
    birth_date = models.DateField() 
    fortune_date = models.DateField(auto_now_add=True)
    
    # 별자리 데이터 (타로)
    star_name = models.CharField(max_length=20)
    star_text = models.TextField()
    star_score = models.IntegerField()
    
    # 띠 데이터 (명리)
    zodiac_name = models.CharField(max_length=20)
    zodiac_text = models.TextField()
    zodiac_score = models.IntegerField()
    
    class Meta:
        ordering = ['-fortune_date'] # 최신순 정렬

    def __str__(self):
        return f"{self.fortune_date} - {self.star_name}/{self.zodiac_name}"