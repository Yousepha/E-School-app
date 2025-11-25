from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UtilisateurViewSet, EleveViewSet, EnseignantViewSet, ClasseViewSet,
    MatiereViewSet, SalleViewSet, AnneeScolaireViewSet, CoursViewSet,
    InscriptionViewSet, NoteViewSet, PaiementViewSet, AbsenceViewSet,
    ParentEleveViewSet, home
)

router = DefaultRouter()

router.register("utilisateurs", UtilisateurViewSet)
router.register("eleves", EleveViewSet)
router.register("enseignants", EnseignantViewSet)
router.register("classes", ClasseViewSet)
router.register("matieres", MatiereViewSet)
router.register("salles", SalleViewSet)
router.register("annees-scolaires", AnneeScolaireViewSet)
router.register("cours", CoursViewSet)
router.register("inscriptions", InscriptionViewSet)
router.register("notes", NoteViewSet)
router.register("paiements", PaiementViewSet)
router.register("absences", AbsenceViewSet)
router.register("parents-eleves", ParentEleveViewSet)

urlpatterns = [
    path('', home, name='home'),
    path("api/", include(router.urls)),
]
