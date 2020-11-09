from django.contrib.auth.models import User
from django.db import models
from hashid_field import HashidAutoField
from django.utils.translation import gettext as _


class GenericModel(models.Model):
    id = HashidAutoField(primary_key=True)
    dt_criacao = models.DateTimeField(_('Data Criação'), auto_now_add=True)
    dt_update = models.DateTimeField(_('Data Atualização'), auto_now_add=True)

    class Meta:
        abstract = True


class Publication(GenericModel):
    name = models.CharField(_('Nome'), max_length=255)
    author = models.ForeignKey(User, models.CASCADE, verbose_name=(_('Autor')))
    url_image = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Publicação')
        verbose_name_plural = _('Publicações')


class Product(GenericModel):
    publication = models.ForeignKey(Publication, models.CASCADE)
    price = models.DecimalField(_('Preço'), max_digits=6, decimal_places=2)
    quantity_stock = models.IntegerField(_('Quantidade em Estoque'), default=1, null=True, blank=True)

    def __str__(self):
        return str(self.publication)

    class Meta:
        verbose_name = _('Produto')


class Sale(GenericModel):
    product = models.ForeignKey(Product, models.PROTECT, verbose_name=(_('Produto')))
    owner = models.ForeignKey(User, models.PROTECT, verbose_name=(_('Comprador')))
    quantity = models.IntegerField(_('Quantidade'), default=1, null=True, blank=True)
    amount = models.DecimalField(_('Valor Total'), max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Venda'

    def __str__(self):
        return f'{self.product} - {self.owner}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.amount = self.quantity * self.product.price
        super().save(force_insert, force_update, using, update_fields)

