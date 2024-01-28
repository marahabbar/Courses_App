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
import datetime 
from dateutil.relativedelta import relativedelta  
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


    def get(self, request, section_id,mac=None,student_id=None, *args, **kwargs):
        # test enrollment
        try:
           enrolled_section=Enrolled_section.objects.get(mac_address=mac,section_id=section_id,student=student_id)
        except Enrolled_section.DoesNotExist:
            return Response("not enrolled yet", status=status.HTTP_200_OK) 
        if enrolled_section.expiry_date < datetime.datetime.now().date():
            return Response("code is expired", status=status.HTTP_200_OK) 
        
        section_instance = self.get_object(section_id)
        if not section_instance:
            return status.HTTP_400_BAD_REQUEST
        serializer = sectionDetailsSerializer(section_instance)
        section_items = sorted(serializer.data['section_item'], key=lambda d: d['item_order']) 
        if  section_instance.withGroups:
            items_list=[]
            for item in section_items:
                 item_dic={"title":item["title"],"type":item["item_type"]}
                 if item["item_type"]==1:
                    item_dic['item']=item["video"]
                 elif item["item_type"]==2:
                    item_dic['item']=item["assessed_reading"]
                 elif item["item_type"]==3:
                    item_dic['item']=item["quiz"]    
                 added=False
                 for i,group in enumerate(items_list):
                     if item["group"]==items_list[i]["group"]:
                         items_list[i]["items"].append(item_dic)
                         added=True
                 if not added:
                    items_list.append({"group":item["group"],"items":[item_dic]})
   
            
        return Response(items_list, status=status.HTTP_200_OK)
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

    # 5. Delete
    def delete(self, request, Student_id, *args, **kwargs):

        Student_instance = self.get_object(Student_id)
        if not Student_instance:
            return  status.HTTP_400_BAD_REQUEST
            
        Student_instance.delete()
        return status.HTTP_200_OK

class EnrollmentCodeApiView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated] 

    def get(self, request, *args, **kwargs):

            codes = Enrollment_Code.objects.all()
            serializer = Enrollment_CodeSerializer(codes, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = Enrollment_CodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, code_id, *args, **kwargs):
        try:
            code= Enrollment_Code.objects.get(id=code_id)
        except Course.DoesNotExist:
            return status.HTTP_404_NOT_FOUND
        if code.status== 1:
            return  Response("code already sold", status=status.HTTP_200_OK)
        code.status=1
        code.save()
        return Response("code has been sold successfully", status=status.HTTP_200_OK)

class EnrolledSectionApiView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated] 

    def get(self, request,section_id=None, *args, **kwargs):

            Enrolled_sections = Enrolled_section.objects.all()
            serializer =Enrolled_sectionSerializer(Enrolled_sections, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,section_id, *args, **kwargs):
        code=Enrollment_Code.objects.filter(code=request.data['code'],enrolled_section=section_id,status=1)
        if code:
            #enroll
            
            serializer = Enrolled_sectionSerializer(data={"expiry_date": (datetime.datetime.now() +relativedelta(days=code[0].validity_period)).strftime("%Y-%m-%d"),
                                                          "mac_address":request.data['mac_address'],
                                                          "student":request.data['student'],
                                                          "section":section_id
                                                          }
                                                    )
            if serializer.is_valid():
                serializer.save()
                code[0].status=2
                code[0].save()
                return Response("section has been enrolled successfully ", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_200_OK)

        return Response("invalid code", status=status.HTTP_200_OK)

    

class StudentSignUp(generics.CreateAPIView):
    # queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def post(self, request , *args, **kwargs):
        user_serializer = RegisterSerializer(data={
            # username=validated_data['username'],
            "email":request.data['email'],
            "full_name":request.data['full_name'],
            "password":request.data['password']
            # last_name=validated_data['last_name'],
                # is_student=True
                }
        )

        if  user_serializer.is_valid():
            user=user_serializer.save()
            user.set_password(request.data['password'])
            user.is_student=True
            user.save()
            student_serializer=StudentSerializer(data={"full_name":request.data['full_name'],
                "phone":request.data['phone'],
                "user":user.id
                })
            if student_serializer.is_valid():
                student=student_serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                return Response({'id': str(student.id),
                                'access': str(access_token)},status=status.HTTP_200_OK)
            user.delete()
            return Response(student_serializer.errors, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_200_OK)


