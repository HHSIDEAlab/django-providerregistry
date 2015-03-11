from django.db import models

class NameAlias(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    alias = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "%s" % (self.name)
    
    class Meta:
        ordering = ('name','alias')

    def save(self, commit = True, **kwargs):
        
        #Force to Uppercase
        self.name  = self.name.upper()
        self.alias = self.alias.upper()
        
        if commit:
            super(NameAlias, self).save(**kwargs)