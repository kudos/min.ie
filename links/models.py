from django.db import models
from django.forms import ModelForm, CharField, TextInput
import random


class Link(models.Model):
  id = models.CharField(primary_key=True, max_length=12)
  url = models.URLField(max_length=2048)
  created_at = models.DateTimeField(auto_now_add=False)
  clicks = models.IntegerField(default=0)
  ip = models.GenericIPAddressField(null=True)

  def __unicode__(self):
    return self.url

  def generate_unique_id(self, length=8):
    attempts = 0
    id = random_id(length)
    try:
      while Link.objects.get(id=id) and attempts < 10:
        attempts = attempts + 1
        id = random_id()
    except:
      pass
    return id
    
  def save(self, *args, **kwargs):
    if not self.pk:
      self.id = self.generate_unique_id()
    super(Link, self).save(*args, **kwargs)


class LinkForm(ModelForm):
  url = CharField(label='')
  class Meta:
    model = Link
    fields = ['url']
      

def random_id(length):
  rand = ''
  for i in range(0,length):
    rand += int_to_char(random.randint(0,61));
  return rand;


def int_to_char(int):
  if(int < 10):
    char = chr(int + 48)
  elif(int < 36):
    char = chr(int + 55)
  else:
    char = chr(int + 61)
  return char