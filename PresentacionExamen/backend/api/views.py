from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from datetime import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import F, OuterRef, Subquery, Sum
from .models import (
    Asignaturas,
    Corresponde,
    Crea,
    Cursa,
    Estudiantes,
    Evalua,
    Imparte,
    Ingresa,
    Preguntas,
    Profesores,
    Programa,
    Responde,
    Respuestas,
    Salones,
    Selecciona,
    Tipospreguntas,
)

from .serializers import (
    AsignaturaSerializer,
    CorrespondeSerializer,
    CreaSerializer,
    CursaSerializer,
    EstudianteSerializer,
    EvaluaSerializer,
    ImparteSerializer,
    IngresaSerializer,
    PreguntasSerializer,
    ProfesoresSerializer,
    ProgramaSerializer,
    RespondeSerializer,
    RespuestasSerializer,
    SalonesSerializer,
    SeleccionaSerializer,
    TipospreguntasSerializer,
    UserSerializer
)

USER_TYPES = {
    'estudiante': 1,
    'docente': 2
}

QUESTION_TYPES = {
    'multiselect-multichoice': 1,
    'multiselect-singlechoice': 2,
    'true-false': 3,
}

class ApiViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Base entry point. please specify in the path the resource you want to use."})

class AuthViewSet(ViewSet):
    # POST - Validate user
    def create(self, request):
        try:
            # Extraer encabezados
            user_code = request.query_params.get('X-Code')
            password = request.data.get('password')

            print('user_code',user_code)
            print('password',password)
            if not user_code or not password:
                raise AuthenticationFailed("Credenciales inválidas.")

            # Autenticar el usuario buscando en ambas tablas
            user = Estudiantes.objects.filter(cod_estudiante=user_code).first()
            user_type = 1  # Estudiante

            if user:
                user_password = user.pw_estudiante
                user_active = user.activo_estudiante
                user_name = user.nom_estudiante
            else:
                user = Profesores.objects.filter(cod_profesor=user_code).first()
                user_type = 2  # Docente
                user_password = user.pw_profesor if user else None
                user_active = user.activo_profesor if user else False
                user_name = user.nom_profesor if user else ""

            if not user:
                raise AuthenticationFailed("Usuario no encontrado.")

            print('user_password',user_password)
            # Validar contraseña
            if password != user_password:
                raise AuthenticationFailed("Contraseña incorrecta.")

            # Respuesta de éxito
            response_data = {
                "isActive": user_active,
                "userType": user_type,
                "Name": user_name,
                "id": user_code
            }
            return Response(response_data, status=200)

        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=401)

        except Exception as e:
            return Response({"error": f"Error al autenticar: {str(e)}"}, status=500)

class ExamQuestionaireViewSet(ViewSet):
    # GET - pull questionaire questions based on exam_id provided
    def retrieve(self, request, pk=None):
        try:
            # Obtener la información básica del examen desde Crea
            crea_entries = Crea.objects.filter(id_examen=pk).select_related('tipo_examen')

            if not crea_entries.exists():
                return Response({"error": "El examen no existe."}, status=404)

            crea_entry = crea_entries.first()

            # Obtener las preguntas relacionadas al examen
            preguntas_ids = crea_entries.values_list('id_pregunta', flat=True)

            preguntas = Preguntas.objects.filter(id_pregunta__in=preguntas_ids)

            # Calcular la duración total del examen sumando los tiempos de las preguntas desde Ingresa
            total_duration = Ingresa.objects.filter(
                id_pregunta__in=preguntas_ids
            ).aggregate(total_time=Sum('tiempo_pregunta'))['total_time'] or 0

            # Construir la lista de preguntas con sus opciones
            questions_list = []
            for pregunta in preguntas:
                opciones = Corresponde.objects.filter(id_pregunta=pregunta.id_pregunta).select_related('id_respuesta')
                options_list = [
                    {
                        "idOption": opcion.id_respuesta.id_respuesta,
                        "textOption": opcion.id_respuesta.desc_respuesta
                    }
                    for opcion in opciones
                ]

                questions_list.append({
                    "idQuestion": pregunta.id_pregunta,
                    "typeQuestion": pregunta.tipo_pregunta.id_tipo_pregunta,
                    "questionStatement": pregunta.desc_pregunta,
                    "options": options_list
                })

            # Construir la respuesta del examen
            exam_data = {
                "idExam": crea_entry.id_examen,
                "subject": crea_entry.cod_asignatura,
                "duration": total_duration,
                "isProgrammed": crea_entry.examen_finalizado,
                "typeExam": crea_entry.tipo_examen.id_tipo_examen,
                "questions": questions_list
            }

            return Response({"exam": exam_data}, status=200)

        except Exception as e:
            return Response({"error": f"Error al obtener el cuestionario del examen: {str(e)}"}, status=500)

    # GET - pull all questionaire ???
    def list(self, request):
        o_data = {
            }
        return Response(o_data)

class ExamScheduledViewSet(ViewSet):
    # GET - Retrieve exam scheduled data
    def list(self, request):
        teacher_id = request.query_params.get('teacher_id', None)
        student_id = request.query_params.get('student_id', None)
        subject = request.query_params.get('subject_id', None)

        if not subject or (not teacher_id and not student_id):
            return Response(
                {"error": "Los encabezados 'teacher_id' o 'student_id' y 'subject' son obligatorios."},
                status=400
            )

        try:
            # Base query: filtrar exámenes por asignatura
            exams = Programa.objects.filter(cod_asignatura=subject)

            # Filtrar por docente
            if teacher_id:
                exams = exams.filter(cod_profesor=teacher_id)

            # Filtrar por estudiante
            elif student_id:
                exams = exams.filter(cod_estudiante=student_id)

            if not exams.exists():
                return Response(
                    {"examList": []},
                    status=200
                )

            exam_list = []
            for exam in exams:
                # Obtener información del salón y tipo de examen desde Crea
                crea_entry = Crea.objects.filter(
                    id_examen=exam.id_examen
                ).select_related('tipo_examen').first()

                # Obtener preguntas relacionadas al examen desde Corresponde -> Ingresa
                preguntas = Corresponde.objects.filter(
                    id_pregunta=exam.id_pregunta
                )

                # Calcular duración sumando tiempos desde Ingresa
                total_duration = Ingresa.objects.filter(
                    id_pregunta__in=preguntas.values_list('id_pregunta', flat=True)
                ).aggregate(total_time=Sum('tiempo_pregunta'))['total_time'] or 0

                # Construir el diccionario para el examen
                exam_data = {
                    "subject": exam.cod_asignatura,
                    "subjectName": exam.cod_asignatura.nombre_asignatura if hasattr(exam.cod_asignatura, 'nombre_asignatura') else "",
                    "date": f"{exam.fecha_examen} {exam.hora_examen}",
                    "salonNum": crea_entry.id_salon if crea_entry else "",
                    "salonBuilding": "",  # Campo no definido
                    "numQuestions": preguntas.count(),
                    "duration": total_duration,
                    "isProgrammed": True
                }

                # Agregar tipo_examen si es estudiante
                if student_id and crea_entry:
                    exam_data["examType"] = crea_entry.tipo_examen.id_tipo_examen if crea_entry.tipo_examen else None

                exam_list.append(exam_data)

            # Respuesta final
            response_data = {
                "examList": exam_list
            }

            return Response(response_data, status=200)

        except Exception as e:
            return Response(
                {"error": f"Error al obtener los exámenes: {str(e)}"},
                status=500
            )

        return Response(o_data)

    # POST - scheduled an exam
    def create(self, request):
        s_subject_id = request.query_params.get('subject_id', None)
        s_student_id = request.query_params.get('student_id', None)

        # Instancia clase
        # Llamado metodo para obtener info de examenes
        o_data = {
                "status": 200,
                "message": "Examen programado con exito",
                "isCreate": True
            }
        return Response(o_data)

    # PUT - Update scheduled exam
    def update(self, request):
        s_subject_id = request.query_params.get('subject_id', None)
        s_student_id = request.query_params.get('student_id', None)

        # Instancia clase
        # Llamado metodo para obtener info de examenes
        o_data = {
                "status": 200,
                "message": "Examen reprogramado con exito",
                "isCreate": True
            }
        return Response(o_data)

class ExamViewSet(ViewSet):
    # GET - get exam settings based on id
    def list(self, request):
        # Leer parámetros de consulta
        subject = request.query_params.get('subject')
        exam_type = request.query_params.get('examType')

        if not subject or not exam_type:
            return Response(
                {"error": "Los parámetros 'subject' y 'examType' son obligatorios."},
                status=400
            )

        try:
            # Buscar el examen con la combinación de asignatura y tipo de examen
            exam = Crea.objects.filter(
                cod_asignatura=subject,
                tipo_examen=exam_type
            ).values('id_examen').first()

            # Si el examen ya existe
            if exam:
                return Response({
                    "status": 200,
                    "message": "La configuración del examen ya existe",
                    "available": False,
                    "id_examen": exam['id_examen']
                }, status=200)

            # Si el examen no existe
            return Response({
                "status": 200,
                "message": "La configuración del examen puede ser creada",
                "available": True
            }, status=200)

        except Exception as e:
            return Response(
                {"error": f"Error al verificar el examen: {str(e)}"},
                status=500
            )

    # POST - create an exam
    def create(self, request):
        o_data = {
                "status": 200,
                "message": "Examen creado con exito",
                "isCreate": True
            }
        return Response(o_data)

    # PUT - edit exam info
    def update(self, request):
        o_data = {
                "status": 200,
                "message": "Examen editado con exito",
                "isCreate": True
            }
        return Response(o_data)

class NotesViewSet(ViewSet):
    # GET - retrieve notes based on role and subject
    def list(self, request):

        #student notes
        o_data = {
            "notesStudent": [
                {
                "group": 230,
                "subject": 120,
                "typeExam": 1,
                "subjectName": "Calculo Diferencial",
                "date": "Mon Nov 20 2024 06:12:45 GMT-0500",
                "note": 43,
                "state": "Aprobado"
                },
                {
                "group": 230,
                "subject": 150,
                "typeExam": 1,
                "subjectName": "Base de datos",
                "date": "Tue Nov 21 2024 18:05:33 GMT-0500",
                "note": 43,
                "state": "Aprobado"
                },
                {
                "group": 230,
                "subject": 230,
                "typeExam": 1,
                "subjectName": "Caculo Integral",
                "date": "Tue Nov 21 2024 18:05:33 GMT-0500",
                "note": 43,
                "state": "Aprobado"
                }
            ]
        }

        #teacher notes
        o_data = {
            "notesTeacher": [
                {
                "group:": 120,
                "subject": 150,
                "subjectName": "Base de datos",
                "notesExam": [
                    {
                    "typeExam": 1,
                    "date": "Mon Nov 20 2024 06:12:45 GMT-0500"
                    },
                    {
                    "typeExam": 2,
                    "date": "Tue Nov 21 2024 18:05:33 GMT-0500"
                    }
                ]
                },
                {
                "group:": 120,
                "subject": 210,
                "subjectName": "Ingeniería de software 1",
                "notesExam": [
                    {
                    "typeExam": 1,
                    "date": "Mon Nov 20 2024 06:12:45 GMT-0500"
                    }
                ]
                }
            ]
        }

        #subject notes
        o_data = {
            "subject": 120,
            "subjectName": "Base de datos",
            "date": "Mon Nov 20 2024 06:12:45 GMT-0500",
            "numQuestions": 5,
            "numStudents": 3,
            "notesSubject": [
                {
                    "idStudent": 20241595005,
                    "nameStudent": "Gabriela Leon",
                    "note": 43,
                    "answerStudent": [
                        {
                        "idQuestion": 1,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 2,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 3,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 4,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 5,
                        "isCorrect": false
                        }
                    ]
                },
                {
                    "idStudent": 20241595004,
                    "nameStudent": "Edwin Guevara",
                    "note": 39,
                    "answerStudent": [
                        {
                        "idQuestion": 1,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 2,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 3,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 4,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 5,
                        "isCorrect": false
                        }
                    ]
                },
                {
                    "idStudent": 20241595010,
                    "nameStudent": "Rodrigo Perez",
                    "note": 15,
                    "answerStudent": [
                        {
                        "idQuestion": 1,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 2,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 3,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 4,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 5,
                        "isCorrect": True
                        }
                    ]
                }
            ]
        }
        return Response(o_data)

class QuestionViewSet(ViewSet):
    #get questions per subject
    def list(self, request):
        try:
            subject = request.query_params.get('subject')

            if not subject:
                return Response(
                    {"error": "El parámetro 'subject' es obligatorio."},
                    status=400
                )

            # Subconsulta para obtener el tiempo de cada pregunta desde Ingresa
            tiempo_pregunta_subquery = Ingresa.objects.filter(
                id_pregunta=OuterRef('id_pregunta'),
                cod_asignatura=subject
            ).values('tiempo_pregunta')[:1]

            # Consultar preguntas relacionadas con respuestas y tiempo
            preguntas = Preguntas.objects.filter(
                id_pregunta__in=Ingresa.objects.filter(cod_asignatura=subject).values_list('id_pregunta', flat=True)
            ).annotate(
                tiempo_pregunta=Subquery(tiempo_pregunta_subquery),
                respuesta_id=F('corresponde__id_respuesta'),
                respuesta_descripcion=F('corresponde__id_respuesta__desc_respuesta'),
                es_correcta=F('corresponde__correcta')
            ).values(
                'id_pregunta',
                'desc_pregunta',
                'tipo_pregunta',
                'tiempo_pregunta',
                'respuesta_id',
                'respuesta_descripcion',
                'es_correcta'
            )

            if not preguntas.exists():
                return Response(
                    {"error": f"No se encontraron preguntas para la asignatura con ID {subject}."},
                    status=404
                )

            # Agrupar preguntas y sus opciones
            questions_list = {}
            for pregunta in preguntas:
                id_pregunta = pregunta['id_pregunta']
                if id_pregunta not in questions_list:
                    questions_list[id_pregunta] = {
                        "idQuestion": id_pregunta,
                        "typeQuestion": pregunta['tipo_pregunta'],
                        "timeQuestion": pregunta['tiempo_pregunta'],
                        "questionStatement": pregunta['desc_pregunta'],
                        "options": []
                    }

                questions_list[id_pregunta]["options"].append({
                    "idOption": pregunta['respuesta_id'],
                    "textOption": pregunta['respuesta_descripcion']
                })

            # Convertir el diccionario en una lista dentro de la clave `questionsList`
            response_data = {
                "questionsList": list(questions_list.values())
            }

            return Response(response_data, status=200)

        except Exception as e:
            return Response(
                {"error": f"Error al obtener las preguntas: {str(e)}"},
                status=500
            )

    # GET - retrieve question per question_id
    def retrieve(self, request, pk=None):
        try:
            # Subconsulta para obtener el tiempo de la pregunta desde `Ingresa`
            tiempo_pregunta_subquery = Ingresa.objects.filter(
                id_pregunta=pk
            ).values('tiempo_pregunta')[:1]

            # Obtener la pregunta con sus respuestas y el tiempo
            pregunta = Preguntas.objects.filter(id_pregunta=pk).annotate(
                tiempo_pregunta=Subquery(tiempo_pregunta_subquery),
                respuesta_id=F('corresponde__id_respuesta'),
                respuesta_descripcion=F('corresponde__id_respuesta__desc_respuesta'),
                es_correcta=F('corresponde__correcta')
            ).values(
                'id_pregunta',
                'desc_pregunta',
                'tipo_pregunta',
                'tiempo_pregunta',
                'respuesta_id',
                'respuesta_descripcion',
                'es_correcta'
            )

            if not pregunta.exists():
                return Response(
                    {"error": f"No se encontró la pregunta con ID {pk}."},
                    status=404
                )

            # Construir la pregunta con opciones
            question = {
                "idQuestion": pk,
                "typeQuestion": pregunta[0]['tipo_pregunta'],  # Tipo de pregunta
                "timeQuestion": pregunta[0]['tiempo_pregunta'],  # Tiempo de la pregunta
                "questionStatement": pregunta[0]['desc_pregunta'],  # Enunciado
                "options": [
                    {
                        "idOption": p['respuesta_id'],
                        "textOption": p['respuesta_descripcion']
                    }
                    for p in pregunta
                ]
            }

            # Respuesta final
            response_data = {"questionsList": [question]}

            return Response(response_data, status=200)

        except Exception as e:
            return Response(
                {"error": f"Error al obtener la pregunta: {str(e)}"},
                status=500
            )

    # POST - create question
    def create(self, request):
        o_data = {
                "status": 200,
                "message": "La pregunta fue creada correctamente",
                "isCreate": True
            }
        return Response(o_data)

class SalonViewSet(ViewSet):
    # GET - list available salon info, based on id, or date provided in body
    def list(self, request):
         # Obtener los parámetros de consulta
        date = request.query_params.get('date')
        time = request.query_params.get('time')

        # Validar parámetros
        if not date or not time:
            return Response(
                {"error": "Los parámetros 'date' y 'time' son obligatorios."},
                status=400
            )

        # Convertir los parámetros a tipos datetime
        try:
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            query_time = datetime.strptime(time, "%H:%M:%S").time()
        except ValueError:
            return Response(
                {"error": "El formato de 'date' debe ser 'YYYY-MM-DD' y 'time' debe ser 'HH:MM'."},
                status=400
            )

        # Obtener los exámenes programados en la fecha y hora dadas
        programas_en_horario = Programa.objects.filter(
            fecha_examen=query_date,
            hora_examen__lte=query_time
        )

        # print("Programas encontrados:")
        # for programa in programas_en_horario:
        #     print(f"ID Examen: {programa.id_examen}, Fecha: {programa.fecha_examen}, Hora: {programa.hora_examen}")

        # Obtener los salones ocupados asociados a esos exámenes
        salones_ocupados = Crea.objects.filter(
            id_examen__in=programas_en_horario.values_list('id_examen', flat=True)
        ).exclude(id_salon__isnull=True).values_list('id_salon', flat=True)

        #print("Salones ocupados encontrados:", list(salones_ocupados))

        # Verificar si hay salones ocupados
        if salones_ocupados.exists():
            # Filtrar los salones disponibles
            salones_disponibles = Salones.objects.exclude(id_salon__in=salones_ocupados)
        else:
            # Si no hay salones ocupados, devolver todos los salones
            salones_disponibles = Salones.objects.all()

        # Construir la respuesta
        response = [
            {"id_salon": salon.id_salon, "capacidad": salon.capacidad}
            for salon in salones_disponibles
        ]

        o_data = {
                "salonList": response
            }

        return Response(o_data)

class SubjectViewSet(ViewSet):
    # GET - subjects info based on teacher_id provided
    def list(self, request):
        # Obtener el teacher_id del header
        teacher_id = request.query_params.get('teacher_id')
        #teacher_id = request.META.get('HTTP_TEACHER_ID')
        #teacher_id = request.headers.get('teacher_id')
        #print('teacher_id',teacher_id)

        if not teacher_id:
            return Response(
                {"error": "El header 'teacher_id' es obligatorio."},
                status=400
            )

        # Filtrar las materias impartidas por el docente
        materias = Imparte.objects.filter(cod_profesor=teacher_id).select_related('cod_asignatura')

        # Verificar si se encontraron resultados
        if not materias.exists():
            return Response(
                {"message": "No se encontraron materias para el docente proporcionado."},
                status=404
            )

        # Serializar los datos
        serialized_materias = AsignaturaSerializer([materia.cod_asignatura for materia in materias], many=True)
        o_data = {
            "subjectList":serialized_materias.data
        }

        return Response(o_data, status=200)