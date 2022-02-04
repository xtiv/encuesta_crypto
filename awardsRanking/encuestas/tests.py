import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Pregunta


# Bateria de test, se le llama así porque hereda de TestCase
class PreguntaModelTests(TestCase):
    
    def create_question(self, time):
        """ Create a question to run tests
            
            Parameter:
            - time : timezone
            
            Returns
            - a question
        """
        return Pregunta(pregunta_text="¿am i a time traveler?", pub_date=time)

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns Falses for questions whose pub_date is in the future """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question= self.create_question(time)
        
        self.assertIs(future_question.was_published_recently(),False)
        
    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns Falses for questions whose pub_date is in the Present """
        time = timezone.now()
        present_question = self.create_question(time)
        
        self.assertIs(present_question.was_published_recently(), True)
        
    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns Falses for questions whose pub_date is in the Past """
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = self.create_question(time)
        
        self.assertIs(past_question.was_published_recently(), False)
        
def crear_pregunta(dias):
    time= timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(pregunta_text='a quesiton?', pub_date=time)

        
class PreguntaIndexViewTests(TestCase):
    def test_no_questions(self):
        ## Con self.client.get(reverse("x:x")) hacemos peticiones http al template indicado
        response = self.client.get(reverse("encuestas:index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        ## Asignamos el contexto a response y en el querysetequal indicamos que sea igual a una lista vacía
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future(self):
        crear_pregunta(30)
        response = self.client.get(reverse("encuestas:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_past(self):
        question= crear_pregunta(-30)
        response= self.client.get(reverse("encuestas:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
    def test_past_and_future_question(self):
        past_question = crear_pregunta(-30)
        future_question = crear_pregunta(30)
        response = self.client.get(reverse("encuestas:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )
        
    def test_two_pasty_questions(self):
        past_questions = Pregunta.objects.create(pregunta_text="tu mama tiene penes", pub_date=timezone.now() - datetime.timedelta(days=20))
        past_questionz = Pregunta.objects.create(pregunta_text="tu mama tiene pene", pub_date=timezone.now() - datetime.timedelta(days=10))
        
        response = self.client.get(reverse("encuestas:index"))
        
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_questionz, past_questions]
        )
        
    def test_two_future_questions(self):
        future_question1 = crear_pregunta(30)
        future_question1 = crear_pregunta(40)
        
        response = self.client.get(reverse("encuestas:index"))
        
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )

class PreguntaDetailViewTest(TestCase):
    def test_future_question(self):
        """
        Returns a 404 error when the client requests a question with pub_date in the future
        """
        future_question = crear_pregunta(30)
        url = reverse("encuestas:detalle_pregunta", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class PreguntaResultViewTest(TestCase):
    def test_future_question(self):
        future_question = crear_pregunta(10)
        url = reverse("encuestas:resultados_pregunta", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
