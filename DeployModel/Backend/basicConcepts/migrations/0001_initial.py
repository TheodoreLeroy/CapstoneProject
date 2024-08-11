# Generated by Django 5.0.7 on 2024-08-10 07:25

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50, unique=True)),
                ('semester', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attend_status', models.BinaryField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('CameraId', models.IntegerField(auto_created=True, default=1, primary_key=True, serialize=False)),
                ('position', models.CharField(max_length=100)),
                ('classId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.class')),
            ],
        ),
        migrations.CreateModel(
            name='AttendentStudentsAtAllFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('total_attendent', models.IntegerField()),
                ('log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.log')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('status', models.BooleanField(default=False)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.class')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='slot_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.slot'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=16)),
                ('embedding', models.BinaryField()),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.class')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teach_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.class')),
                ('slot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.slot')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding', models.BinaryField(default=b'')),
                ('slot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.slot')),
            ],
        ),
        migrations.CreateModel(
            name='AttendentStudentsAtOneFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding', models.JSONField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicConcepts.student')),
                ('time_frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_frame', to='basicConcepts.timeframe')),
            ],
        ),
    ]
