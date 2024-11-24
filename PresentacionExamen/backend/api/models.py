# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Asignaturas(models.Model):
    cod_asignatura = models.IntegerField(primary_key=True)
    nom_asignatura = models.CharField(max_length=50)
    inten_horaria = models.SmallIntegerField()
    credit_asignatura = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'asignaturas'


class Corresponde(models.Model):
    id_pregunta = models.OneToOneField('Preguntas', models.DO_NOTHING, db_column='id_pregunta', primary_key=True)
    id_respuesta = models.ForeignKey('Respuestas', models.DO_NOTHING, db_column='id_respuesta')
    correcta = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'corresponde'
        unique_together = (('id_pregunta', 'id_respuesta'),)


class Crea(models.Model):
    cod_profesor = models.OneToOneField('Imparte', models.DO_NOTHING, db_column='cod_profesor', primary_key=True)
    cod_asignatura = models.IntegerField()
    grupo = models.SmallIntegerField()
    cod_estudiante = models.ForeignKey('Evalua', models.DO_NOTHING, db_column='cod_estudiante')
    id_pregunta = models.IntegerField()
    id_respuesta = models.IntegerField()
    id_examen = models.IntegerField()
    tipo_examen = models.ForeignKey('Tipoexamen', models.DO_NOTHING, db_column='tipo_examen')
    examen_finalizado = models.BooleanField()
    id_salon = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crea'
        unique_together = (('cod_profesor', 'cod_asignatura', 'grupo', 'cod_estudiante', 'id_pregunta', 'id_respuesta', 'id_examen'),)


class Cursa(models.Model):
    cod_estudiante = models.OneToOneField('Estudiantes', models.DO_NOTHING, db_column='cod_estudiante', primary_key=True)
    cod_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='cod_asignatura')

    class Meta:
        managed = False
        db_table = 'cursa'
        unique_together = (('cod_estudiante', 'cod_asignatura'),)


class Estudiantes(models.Model):
    cod_estudiante = models.BigIntegerField(primary_key=True)
    nom_estudiante = models.CharField(max_length=50)
    dir_estudiante = models.CharField(max_length=50)
    tel_estudiante = models.CharField(max_length=10)
    cod_carrera = models.IntegerField()
    fecha_nacimiento = models.DateField()

    class Meta:
        managed = False
        db_table = 'estudiantes'


class Evalua(models.Model):
    cod_estudiante = models.OneToOneField(Cursa, models.DO_NOTHING, db_column='cod_estudiante', primary_key=True)
    cod_asignatura = models.IntegerField()
    grupo = models.SmallIntegerField()
    cod_profesor = models.ForeignKey('Imparte', models.DO_NOTHING, db_column='cod_profesor')
    id_pregunta = models.ForeignKey(Corresponde, models.DO_NOTHING, db_column='id_pregunta')
    id_respuesta = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'evalua'
        unique_together = (('cod_estudiante', 'cod_asignatura', 'grupo', 'cod_profesor', 'id_pregunta', 'id_respuesta'),)


class Imparte(models.Model):
    cod_profesor = models.OneToOneField('Profesores', models.DO_NOTHING, db_column='cod_profesor', primary_key=True)
    cod_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='cod_asignatura')
    grupo = models.SmallIntegerField()
    horario = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'imparte'
        unique_together = (('cod_profesor', 'cod_asignatura', 'grupo'),)


class Ingresa(models.Model):
    cod_profesor = models.OneToOneField(Imparte, models.DO_NOTHING, db_column='cod_profesor', primary_key=True)
    cod_asignatura = models.IntegerField()
    grupo = models.SmallIntegerField()
    id_pregunta = models.ForeignKey(Corresponde, models.DO_NOTHING, db_column='id_pregunta')
    id_respuesta = models.IntegerField()
    tiempo_pregunta = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'ingresa'
        unique_together = (('cod_profesor', 'cod_asignatura', 'grupo', 'id_pregunta', 'id_respuesta'),)


class Preguntas(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    desc_pregunta = models.TextField()
    tipo_pregunta = models.ForeignKey('Tipospreguntas', models.DO_NOTHING, db_column='tipo_pregunta')

    class Meta:
        managed = False
        db_table = 'preguntas'


class Profesores(models.Model):
    cod_profesor = models.IntegerField(primary_key=True)
    nom_profesor = models.CharField(max_length=50)
    profesion = models.CharField(max_length=50)
    niv_escolaridad = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'profesores'


class Programa(models.Model):
    cod_profesor = models.OneToOneField(Crea, models.DO_NOTHING, db_column='cod_profesor', primary_key=True)
    cod_asignatura = models.IntegerField()
    grupo = models.SmallIntegerField()
    cod_estudiante = models.BigIntegerField()
    id_pregunta = models.IntegerField()
    id_respuesta = models.IntegerField()
    id_examen = models.IntegerField()
    fecha_examen = models.DateField()
    hora_examen = models.TimeField()

    class Meta:
        managed = False
        db_table = 'programa'
        unique_together = (('cod_profesor', 'cod_asignatura', 'grupo', 'cod_estudiante', 'id_pregunta', 'id_respuesta', 'id_examen'),)


class Responde(models.Model):
    cod_profesor = models.OneToOneField(Crea, models.DO_NOTHING, db_column='cod_profesor', primary_key=True)
    cod_asignatura = models.IntegerField()
    grupo = models.SmallIntegerField()
    cod_estudiante = models.BigIntegerField()
    id_pregunta = models.ForeignKey(Corresponde, models.DO_NOTHING, db_column='id_pregunta')
    id_respuesta = models.IntegerField()
    id_examen = models.IntegerField()
    fecha_envio_examen = models.DateField()

    class Meta:
        managed = False
        db_table = 'responde'
        unique_together = (('cod_profesor', 'cod_asignatura', 'grupo', 'cod_estudiante', 'id_pregunta', 'id_respuesta', 'id_examen'),)


class Respuestas(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    desc_respuesta = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'respuestas'


class Salones(models.Model):
    id_salon = models.AutoField(primary_key=True)
    capacidad = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'salones'


class Selecciona(models.Model):
    cod_profesor = models.OneToOneField(Crea, models.DO_NOTHING, db_column='cod_profesor', primary_key=True)
    cod_asignatura = models.IntegerField()
    grupo = models.SmallIntegerField()
    cod_estudiante = models.BigIntegerField()
    id_pregunta = models.ForeignKey(Corresponde, models.DO_NOTHING, db_column='id_pregunta')
    id_examen = models.IntegerField()
    id_respuesta = models.IntegerField()
    resp_seleccionada = models.IntegerField()
    fecha_seleccion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'selecciona'
        unique_together = (('cod_profesor', 'cod_asignatura', 'grupo', 'cod_estudiante', 'id_pregunta', 'id_examen', 'resp_seleccionada'),)


class Tipoexamen(models.Model):
    id_tipo_examen = models.IntegerField(primary_key=True)
    nombre_tipo_examen = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipoexamen'


class Tipospreguntas(models.Model):
    id_tipo_pregunta = models.IntegerField(primary_key=True)
    nombre_tipo = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tipospreguntas'
