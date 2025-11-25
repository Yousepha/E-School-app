from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from rest_framework import viewsets
from .models import (
    Absense, AnneeScolaire, Classe, Cours, Eleve, Enseignant,
    Inscription, Matiere, Note, Paiement, ParentEleve, Salle, Utilisateur
)
from .serializers import (
    AbsenceSerializer, AnneeScolaireSerializer, ClasseSerializer, CoursSerializer,
    EleveSerializer, EleveDetailSerializer, EnseignantSerializer, InscriptionSerializer,
    MatiereSerializer, NoteSerializer, PaiementSerializer, ParentEleveSerializer,
    SalleSerializer, UtilisateurSimpleSerializer
)


# ---------------------------
# USERS (Utilisateurs)
# ---------------------------
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSimpleSerializer


# ---------------------------
# ELEVE
# ---------------------------
class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all()

    def get_serializer_class(self):
        # détail avec parents intégrés
        if self.action in ["retrieve"]:
            return EleveDetailSerializer
        return EleveSerializer


# ---------------------------
# ENSEIGNANT
# ---------------------------
class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer


# ---------------------------
# CLASSE
# ---------------------------
class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer


# ---------------------------
# MATIERE
# ---------------------------
class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer


# ---------------------------
# SALLE
# ---------------------------
class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer


# ---------------------------
# ANNEE SCOLAIRE
# ---------------------------
class AnneeScolaireViewSet(viewsets.ModelViewSet):
    queryset = AnneeScolaire.objects.all()
    serializer_class = AnneeScolaireSerializer


# ---------------------------
# COURS
# ---------------------------
class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer


# ---------------------------
# INSCRIPTION
# ---------------------------
class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer


# ---------------------------
# NOTE
# ---------------------------
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


# ---------------------------
# PAIEMENT
# ---------------------------
class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer


# ---------------------------
# ABSENCE
# ---------------------------
class AbsenceViewSet(viewsets.ModelViewSet):
    queryset = Absense.objects.all()
    serializer_class = AbsenceSerializer


# ---------------------------
# PARENT - ELEVE (si tu le gardes)
# ---------------------------
class ParentEleveViewSet(viewsets.ModelViewSet):
    queryset = ParentEleve.objects.all()
    serializer_class = ParentEleveSerializer

def home(request):
    return JsonResponse({"message": "API E-School OK"})