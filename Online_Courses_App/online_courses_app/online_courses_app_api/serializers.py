from datetime import timedelta
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_auth.registration.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from .models import *
from rest_framework.response import Response


# class InstructorSignUpSerializer(RegisterSerializer):
#     instructor = serializers.PrimaryKeyRelatedField(read_only=True,) #by default allow_null = False
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     email = serializers.CharField(required=True)
    
#     def get_cleaned_data(self):
#             data = super(InstructorSignUpSerializer, self).get_cleaned_data()
#             extra_data = {
#                 'first_name' : self.validated_data.get('first_name', ''),
#                 'last_name' : self.validated_data.get('last_name', ''),
#                 'email': self.validated_data.get('email', ''),            }
#             data.update(extra_data)
#             return data

#     def save(self, request):
#         user = super(InstructorSignUpSerializer, self).save(request)
#         user.is_teacher = True
#         user.save()
#         buyer = Instructor(instructor=user,first_name=self.cleaned_data.get('first_name'), 
#                 last_name=self.cleaned_data.get('last_name'),
#                 email=self.cleaned_data.get('email'))
#         buyer.save()
#         return user

class RegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #         required=True,
    #         validators=[UniqueValidator(queryset=User.objects.all())]
    #         )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password','username')
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})

    #     return attrs

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         # username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         # last_name=validated_data['last_name'],
    #         is_student=True
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     refresh = RefreshToken.for_user(user)
    #     access_token = refresh.access_token
    #     access_token.set_exp(lifetime=timedelta(days=200))        
    #     return Response({
    #             'id': str(user.id),
    #             'access': str(access_token),
    #     })

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data
        if self.user.is_student:
            c=Student.objects.filter(user_id=self.user.id)
            if len(c)>0:
                data.update({'id': c[0].id,
                             'full_name':c[0].full_name,
                             'username':self.user.username})
        return data 
    
class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class FacultySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'        

class YearSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'  

class Assessed_ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessed_Reading
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'  

class QuizSerializer(serializers.ModelSerializer):
    Questions = QuestionSerializer(source='question_set', many=True)
    class Meta:
        model = Quiz
        fields = '__all__'
class VideoByGroupSerializer(serializers.ModelSerializer):
    # group = serializers.SerializerMethodField()


    def _build_video_list(group,o):
        videos = Video.objects.filter(group=group)
        serializer = VideoSerializer(videos, many=True)
        return serializer.data

    def get_group(self, obj):
        return self._build_video_list(Video.group)

    class Meta:
        model = Video
        fields =['group']

class sectionItemSerializer(serializers.ModelSerializer):
    video= VideoSerializer() 
    assessed_reading = Assessed_ReadingSerializer() 
    quiz = QuizSerializer() 
    class Meta:
        model = section_item
        fields = '__all__'

class sectionDetailsSerializer(serializers.ModelSerializer):
    # Videos= VideoSerializer(source='video_set', many=True) 
    # Assessed_Reading = Assessed_ReadingSerializer(source='assessed_reading_set', many=True) 
    section_item = sectionItemSerializer(source='section_item_set', many=True)
    class Meta:
        model = section
        fields = '__all__'

class sectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  

class CourseDetailSerializer(serializers.ModelSerializer):
    sections = sectionSerializer(source='section_set', many=True) 
    class Meta:
        model = Course
        fields = '__all__'  

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  

class studiedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = studied
        fields = '__all__'

class Enrolled_sectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrolled_section
        fields = '__all__'    

class Answered_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answered_Question
        fields = '__all__'

class Enrollment_CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment_Code
        fields = '__all__'
