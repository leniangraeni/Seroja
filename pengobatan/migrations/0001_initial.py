# Generated by Django 2.0.1 on 2019-11-28 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JadwalPraktekInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.CharField(choices=[('1', 'Senin'), ('2', 'Selasa'), ('3', 'Rabu'), ('4', 'Kamis'), ('5', 'Jumat'), ('6', 'Sabtu')], max_length=1)),
                ('waktu_mulai', models.TimeField()),
                ('waktu_selesai', models.TimeField()),
                ('dokter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.DokterInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ObatInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=20)),
                ('deskripsi', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PengobatanInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sudah_verifikasi', models.BooleanField(default=False)),
                ('sudah_ditangani', models.BooleanField(default=False)),
                ('sudah_berobat', models.BooleanField(default=False)),
                ('ditolak', models.BooleanField(default=False)),
                ('pesan_penolakan', models.CharField(blank=True, max_length=200)),
                ('tanggal_berkunjung', models.DateField()),
                ('keluhan', models.CharField(max_length=200)),
                ('rujukan', models.ImageField(blank=True, upload_to='rujukan/')),
                ('dosis', models.PositiveIntegerField(default=0)),
                ('aturan', models.CharField(blank=True, max_length=200)),
                ('catatan', models.CharField(blank=True, max_length=200)),
                ('apoteker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.ApotekerInfo')),
                ('dokter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.DokterInfo')),
                ('jadwal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pengobatan.JadwalPraktekInfo')),
                ('obat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pengobatan.ObatInfo')),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PasienInfo')),
                ('petugas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.PetugasInfo')),
            ],
        ),
        migrations.CreateModel(
            name='PoliInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=20)),
                ('penanggung_jawab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.DokterInfo')),
            ],
        ),
        migrations.AddField(
            model_name='jadwalpraktekinfo',
            name='poli',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pengobatan.PoliInfo'),
        ),
    ]
