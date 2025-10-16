from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),  # Thay thế bằng migration cuối cùng của bạn
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')], default='M', max_length=1, null=True, verbose_name='Giới tính'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id_card',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Số CMND/CCCD'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Chức vụ'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='join_date',
            field=models.DateField(blank=True, null=True, verbose_name='Ngày vào làm'),
        ),
    ]