from django.db import models


class Estado(models.Model):
    estado_id = models.CharField(max_length=5, primary_key=True, verbose_name='Código')
    estado = models.CharField(
        max_length=100,
        verbose_name='Nombre del Estado o Departamento',
    )

    def __str__(self):
        return self.estado


class Ciudad(models.Model):
    ciudad_id = models.CharField(max_length=5, primary_key=True, verbose_name='Código')
    estado_id = models.ForeignKey(Estado, on_delete=models.CASCADE)
    ciudad = models.CharField(
        max_length=100,
        verbose_name='Nombre del municipio o ciudad',
    )

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ('estado_id', 'ciudad')

    def __str__(self):
        return f'{self.estado_id} - {self.ciudad}'


class EstructuraOrganica(models.Model):
    COSTOS_CHOICES = [
        ('Centro', 'Centro'),
        ('Unidad', 'Unidad'),
        ('Ninguno', 'Ninguno'),
    ]

    codigo_unidad = models.AutoField(
        primary_key=True,
        verbose_name='Código de la unidad organizacional',
    )
    unidad = models.CharField(
        max_length=100,
        verbose_name='Nombre de la unidad organzacional *',
        blank=False,
        null=False,
    )
    nombre_corto_unidad = models.CharField(
        verbose_name='Nombre corto de la unidad, una sola palabra',
        blank=True,
        null=True,
        max_length=20,
    )
    dependencia_unidad = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subunidades',
        verbose_name='Unidad Superior',
    )
    costos = models.CharField(
        verbose_name='Costos',
        max_length=15,
        choices=COSTOS_CHOICES,
        default='Unidad',
    )
    codigo_contable = models.CharField(
        max_length=10,
        verbose_name='Código contable de costos*',
        blank=True,
        null=True,
    )
    correo_unidad = models.EmailField(
        verbose_name='Correo de la unidad',
        blank=True,
        null=True,
        max_length=155,
    )
    activo = models.BooleanField(
        verbose_name='Estado de la unidad, seleccionado para activo',
        default=True,
    )
    fecha = models.DateField(
        verbose_name='Fecha de Creación',
        blank=True,
        null=True,
        auto_now_add=True,
    )
    user = models.CharField(
        verbose_name='usuario',
        blank=True,
        null=True,
        max_length=155,
    )

    class Meta:
        verbose_name = 'Estructura Orgánica'
        verbose_name_plural = 'Estructura Orgánica'
        ordering = ('unidad',)

    def __str__(self):
        return self.unidad


class Sede(models.Model):
    id_sede = models.AutoField(primary_key=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, verbose_name='Ciudad *')
    nombre_sede = models.CharField(
        verbose_name='Nombre de la sede *',
        blank=False,
        null=False,
        max_length=155,
    )
    direccion = models.CharField(
        verbose_name='dirección de la sede *',
        blank=False,
        null=False,
        max_length=155,
    )
    correo = models.EmailField(
        verbose_name='Correo electrónico *',
        blank=False,
        null=False,
        max_length=155,
    )
    contacto = models.CharField(
        verbose_name='Nombre de contacto *',
        blank=False,
        null=False,
        max_length=155,
    )
    telefono = models.CharField(
        verbose_name='Teléfono *',
        blank=False,
        null=False,
        max_length=155,
    )
    activa = models.BooleanField(verbose_name='Estado de la sede', default=True)
    fecha = models.DateField(
        verbose_name='Fecha de Creación',
        blank=True,
        null=True,
        auto_now_add=True,
    )
    user = models.CharField(
        verbose_name='usuario',
        blank=True,
        null=True,
        max_length=155,
    )

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        ordering = ('nombre_sede',)

    def __str__(self):
        return self.nombre_sede


class Cargo(models.Model):
    id_cargo = models.AutoField(
        primary_key=True,
        null=False,
        blank=False,
        verbose_name='Código del Cargo',
    )
    unidad_estructura = models.ForeignKey(
        EstructuraOrganica,
        verbose_name='Unidad Organizacional a la que se inscribe el cargo *',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    cargo = models.CharField(
        null=False,
        blank=False,
        verbose_name='Descripción del Cargo',
        max_length=255,
    )
    cargo_nombre_corto = models.CharField(
        null=True,
        blank=True,
        verbose_name='Nombre corto del Cargo',
        max_length=20,
    )
    directivo = models.BooleanField(
        verbose_name='Rol del cargo, seleccionado para directivo, no seleccionado para operativo',
        default=True,
    )
    correo_cargo = models.EmailField(
        verbose_name='Correo del cargo',
        blank=True,
        null=True,
        max_length=155,
    )
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, verbose_name='Sede')
    activo = models.BooleanField(
        verbose_name='Estado del cargo, seleccionado para activo',
        default=True,
    )
    fecha = models.DateField(
        verbose_name='Fecha de Creación/modificación',
        blank=False,
        null=False,
        auto_now_add=True,
    )
    user = models.CharField(
        max_length=155,
        verbose_name='usuario',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ('sede', 'unidad_estructura', 'cargo')

    def __str__(self):
        return f'{self.sede} - {self.unidad_estructura} - {self.cargo}'


class Tipodoc(models.Model):
    documento_identidad = models.CharField(
        max_length=30,
        null=False,
        verbose_name='Tipo de documento de identidad *',
    )

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documento'
        ordering = ('documento_identidad',)

    def __str__(self):
        return self.documento_identidad


class Persona(models.Model):
    class Sexogen(models.TextChoices):
        Masculino = 'M'
        Femenino = 'F'
        Otro = 'O'

    class Niveleducativo(models.IntegerChoices):
        Primaria = 1
        Secundaria = 2
        Técnica = 3
        Tecnológica = 4
        Profesional = 5
        Especialización = 6
        Maestría = 7
        Doctorado = 8
        Phd = 9

    identificacion = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name='Numero*',
        null=False,
        blank=False,
    )
    tipodoc = models.ForeignKey(
        Tipodoc,
        on_delete=models.CASCADE,
        verbose_name='Tipo de documento',
    )
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre *',
        null=False,
        blank=False,
    )
    apellidos = models.CharField(
        max_length=50,
        verbose_name='Apellidos *',
        null=False,
        blank=False,
    )
    sexo = models.CharField(choices=Sexogen.choices, blank=True, null=True, verbose_name='Sexo')
    nivelformacion = models.IntegerField(
        choices=Niveleducativo.choices,
        blank=True,
        null=True,
        verbose_name='Nivel de formación alcanzado',
    )
    direccion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Dirección de Residencia',
    )
    barrio = models.CharField(
        max_length=100,
        verbose_name='Barrio de residencia',
        blank=True,
        null=True,
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento',
        blank=True,
        null=True,
    )
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, blank=True, null=True)
    correo_personal = models.EmailField(
        verbose_name='Correo Electrónico Personal',
        blank=True,
        null=True,
    )
    correo_institucional = models.EmailField(
        verbose_name='Correo Electrónico institucional',
        blank=True,
        null=True,
    )
    telefono_fijo = models.CharField(
        max_length=20,
        verbose_name='Teléfono fijo',
        blank=True,
        null=True,
    )
    activo = models.BooleanField(
        verbose_name=(
            'Estado de la persona, solo se deben activar funcionarios, tener en cuenta que '
            'si se inactiva, tambien se inactiva en los cargos asignados y el usuario en la plataforma'
        ),
        default=False,
    )
    celular = models.CharField(
        max_length=20,
        verbose_name='Celular personal',
        blank=True,
        null=True,
    )
    celular_contacto = models.CharField(
        max_length=20,
        verbose_name='Celular de un contacto personal',
        blank=True,
        null=True,
    )
    nombre_contacto = models.CharField(
        max_length=20,
        verbose_name='Nombre del contacto personal',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name='Imagen',
        upload_to='personas_images/',
        blank=True,
        null=True,
    )
    user = models.CharField(
        verbose_name='nombre de usuario en plataforma',
        max_length=150,
        blank=True,
        null=True,
    )
    fecha = models.DateField(
        verbose_name='Fecha de Creación/modificación',
        blank=True,
        null=True,
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ('nombre', 'apellidos')

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'


class FuncionarioCargo(models.Model):
    id_func_cargo = models.AutoField(primary_key=True, null=False, blank=False)
    cargo = models.ForeignKey(
        Cargo,
        verbose_name='Cargo *',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    funcionario = models.ForeignKey(
        Persona,
        verbose_name='Trabajador',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    fecha_cont = models.DateField(verbose_name='Fecha de la asignación', blank=True, null=True)
    estado = models.BooleanField(
        verbose_name='Estado del Trabajador en el cargo, seleccionado para activo',
        default=True,
    )
    fecha_retiro = models.DateField(verbose_name='Fecha de terminación', blank=True, null=True)
    fecha = models.DateField(
        verbose_name='Fecha de Creación/modificación',
        blank=True,
        null=True,
        auto_now_add=True,
    )
    user = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        ordering = ('funcionario', 'cargo')

    def __str__(self):
        return f'{self.funcionario} - {self.cargo}'


class TipoVinculacion(models.Model):
    tipo_vincu_id = models.AutoField(primary_key=True)
    vinculacion = models.CharField(
        verbose_name='Descripción de la vinculación *',
        max_length=20,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Tipo de vinculación'
        verbose_name_plural = 'Tipos de vinculación'
        ordering = ('vinculacion',)

    def __str__(self):
        return self.vinculacion


class PersonaVinculacion(models.Model):
    vincupersona_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    vinculacion = models.ForeignKey(TipoVinculacion, on_delete=models.CASCADE)
    activo = models.BooleanField(verbose_name='Estado del rol, seleccionado para activo', default=True)
    fecha = models.DateField(
        verbose_name='Fecha de Creación/modificación',
        blank=True,
        null=True,
        auto_now_add=True,
    )
    user = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        verbose_name = 'Vinculación de persona'
        verbose_name_plural = 'Vinculaciones de personas'
        ordering = ('persona', 'vinculacion')

    def __str__(self):
        return f'{self.persona} - {self.vinculacion}'


class TipoVisita(models.Model):
    tipo_visita_id = models.AutoField(primary_key=True)
    tipo_visita = models.CharField(
        verbose_name='Tipo de Visita *',
        max_length=60,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Tipo de visita'
        verbose_name_plural = 'Tipos de visita'
        ordering = ('tipo_visita',)

    def __str__(self):
        return self.tipo_visita
