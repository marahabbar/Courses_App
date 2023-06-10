from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import  JWTAuthentication
from .models import *
from .serializers import *
from rest_framework import generics

# Create your views here.

class CourseApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get(self, request, *args, **kwargs):

            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get_object(self, course_id):

        try:
            return Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return status.HTTP_404_NOT_FOUND


    def get(self, request, course_id, *args, **kwargs):

        course_instance = self.get_object(course_id)
        if not course_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = CourseDetailSerializer(course_instance)
        return Response({'id':serializer.data["id"],
                         'name':serializer.data["name"],
                         'description':serializer.data["description"],
                         'sections_count':len(serializer.data["sections"]),
                         'sections':serializer.data["sections"],
                         'price':serializer.data["price"],
                         'duration':serializer.data["Duration"],
                         'image':serializer.data["Image"],

                        }, status=status.HTTP_200_OK)
    # 4. Update
    def put(self, request, course_id, *args, **kwargs):

        course_instance = self.get_object(course_id)
        if not course_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = CourseSerializer(instance = course_instance, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, course_id, *args, **kwargs):

        course_instance = self.get_object(course_id)
        if not course_instance:
            return  status.HTTP_400_BAD_REQUEST
            
        course_instance.delete()
        return status.HTTP_200_OK


class sectionDetailApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get_object(self,section_id):

        try:
            return section.objects.get(id=section_id)
        except section.DoesNotExist:
            return status.HTTP_404_NOT_FOUND


    def get(self, request, section_id, *args, **kwargs):

        section_instance = self.get_object(section_id)
        if not section_instance:
            return status.HTTP_400_BAD_REQUEST
        serializer = sectionDetailsSerializer(section_instance)
        if  section_instance.withGroups:
            videos_list=[]
            for video in serializer.data['Videos']:
                 videos_dic={"id" : video["id"],"url":video["url"],"title":video["title"]}
                 added=False
                 for i,group in enumerate(videos_list):
                     if video["group"]==videos_list[i]["group"]:
                         videos_list[i]["videos"].append(videos_dic)
                         added=True
                 if not added:
                    videos_list.append({"group":video["group"],"videos":[videos_dic]})
            serializer.data["Videos"].extend(videos_list)
            del serializer.data["Videos"][0] 
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 4. Update
    def put(self, request, section_id, *args, **kwargs):

        section_instance = self.get_object(section_id)
        if not section_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = sectionSerializer(instance = section_instance, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, section_id, *args, **kwargs):

        section_instance = self.get_object(section_id)
        if not section_instance:
            return  status.HTTP_400_BAD_REQUEST
            
        section_instance.delete()
        return status.HTTP_200_OK


class InstructorApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 
    
    def get(self, request, *args, **kwargs):

            instructors = Instructor.objects.all()
            serializer = InstructorSerializer(instructors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstructorDetailApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get_object(self, Instructor_id):

        try:
            return Instructor.objects.get(id=Instructor_id)
        except Instructor.DoesNotExist:
            return status.HTTP_404_NOT_FOUND


    def get(self, request, Instructor_id, *args, **kwargs):

        Instructor_instance = self.get_object(Instructor_id)
        if not Instructor_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = InstructorSerializer(Instructor_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, Instructor_id, *args, **kwargs):

        Instructor_instance = self.get_object(Instructor_id)
        if not Instructor_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = CourseSerializer(instance = Instructor_instance, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, Instructor_id, *args, **kwargs):

        Instructor_instance = self.get_object(Instructor_id)
        if not Instructor_instance:
            return  status.HTTP_400_BAD_REQUEST
            
        Instructor_instance.delete()
        return status.HTTP_200_OK

class StudentApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get(self, request, *args, **kwargs):

            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailApiView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get_object(self, Student_id):

        try:
            return Student.objects.get(id=Student_id)
        except Student.DoesNotExist:
            return status.HTTP_404_NOT_FOUND


    def get(self, request, Student_id, *args, **kwargs):

        Student_instance = self.get_object(Student_id)
        if not Student_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = StudentSerializer(Student_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, Student_id, *args, **kwargs):

        Student_instance = self.get_object(Student_id)
        if not Student_instance:
            return status.HTTP_400_BAD_REQUEST

        serializer = CourseSerializer(instance = Student_instance, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Deletehjk
    4
    def delete(self, request, Student_id, *args, **kwargs):

        Student_instance = self.get_object(Student_id)
        if not Student_instance:
            return  status.HTTP_400_BAD_REQUEST
            
        Student_instance.delete()
        return status.HTTP_200_OK


class StudentSignUp(generics.CreateAPIView):
    # queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def post(self, request , *args, **kwargs):
        user = User.objects.create(
            # username=validated_data['username'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            # last_name=validated_data['last_name'],
            is_student=True
        )
        user.set_password(request.POST['password'])
        user.save()
        
        student= Student.objects.create(
            first_name=request.POST['first_name'],
            last_name='',
            user_id=user.id
        )  
        student.save()
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
                'id': str(student.id),
                'access': str(access_token)})


