from rest_framework import serializers
from .models import (
    Absense, AnneeScolaire, Classe, Cours, Eleve, Enseignant,
    Inscription, Matiere, Note, Paiement, ParentEleve, Salle, Utilisateur
)


# --------------------
# Serializers simples
# --------------------
class AnneeScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeScolaire
        fields = ["id", "date_debut", "date_fin"]


class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ["id", "nom", "nombre_eleve"]


class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ["id", "nom", "coef"]


class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ["id", "nom", "capacite"]


class EnseignantSerializer(serializers.ModelSerializer):
    admin_id = serializers.PrimaryKeyRelatedField(
        source="admin", queryset=Utilisateur.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Enseignant
        fields = [
            "id", "nom", "prenom", "adresse", "email", "photo", "telephone",
            "login", "password", "type_profil", "matricule", "grade",
            "date_affiliation", "admin_id"
        ]
        extra_kwargs = {"password": {"write_only": True}}


# --------------------
# Utilisateur <-> Eleve
# --------------------
class UtilisateurSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ["id", "nom", "prenom", "email", "telephone", "photo"]


class EleveSerializer(serializers.ModelSerializer):
    # envoyer/recevoir parents par ID (list d'IDs)
    parents = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Utilisateur.objects.all(), required=False
    )
    admin_id = serializers.PrimaryKeyRelatedField(
        source="admin", queryset=Utilisateur.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Eleve
        fields = [
            "id", "nom", "prenom", "adresse", "email", "photo", "telephone",
            "login", "password", "type_profil", "numero_eleve", "admin_id", "parents"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        parents = validated_data.pop("parents", [])
        admin = validated_data.pop("admin", None)
        eleve = Eleve.objects.create(**validated_data, admin=admin)
        if parents:
            eleve.parents.set(parents)
        return eleve

    def update(self, instance, validated_data):
        parents = validated_data.pop("parents", None)
        admin = validated_data.pop("admin", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.admin = admin if admin is not None else instance.admin
        instance.save()
        if parents is not None:
            instance.parents.set(parents)
        return instance


# Variante : si tu veux retourner les objets parents complets (nested) en lecture :
class EleveDetailSerializer(EleveSerializer):
    parents = UtilisateurSimpleSerializer(many=True, read_only=True)
    admin = UtilisateurSimpleSerializer(read_only=True)


# --------------------
# Cours, Inscription, Note, Paiement, Absence
# --------------------
class CoursSerializer(serializers.ModelSerializer):
    enseignant_id = serializers.PrimaryKeyRelatedField(
        source="enseignant", queryset=Enseignant.objects.all()
    )
    matiere_id = serializers.PrimaryKeyRelatedField(
        source="matiere", queryset=Matiere.objects.all()
    )
    classe_id = serializers.PrimaryKeyRelatedField(
        source="classe", queryset=Classe.objects.all()
    )
    salle_id = serializers.PrimaryKeyRelatedField(
        source="salle", queryset=Salle.objects.all()
    )

    class Meta:
        model = Cours
        fields = [
            "id", "heure_debut", "heure_fin", "jour",
            "enseignant_id", "matiere_id", "classe_id", "salle_id"
        ]


class InscriptionSerializer(serializers.ModelSerializer):
    eleve_id = serializers.PrimaryKeyRelatedField(source="eleve", queryset=Eleve.objects.all())
    classe_id = serializers.PrimaryKeyRelatedField(source="classe", queryset=Classe.objects.all())
    annee_scolaire_id = serializers.PrimaryKeyRelatedField(
        source="annee_scolaire", queryset=AnneeScolaire.objects.all()
    )

    class Meta:
        model = Inscription
        fields = ["id", "date", "cycle", "eleve_id", "classe_id", "annee_scolaire_id"]


class NoteSerializer(serializers.ModelSerializer):
    matiere_id = serializers.PrimaryKeyRelatedField(source="matiere", queryset=Matiere.objects.all())
    eleve_id = serializers.PrimaryKeyRelatedField(source="eleve", queryset=Eleve.objects.all())

    class Meta:
        model = Note
        fields = [
            "id", "devoir", "composition", "examen", "semestre",
            "matiere_id", "eleve_id"
        ]


class PaiementSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(source="parent", queryset=Utilisateur.objects.all())

    class Meta:
        model = Paiement
        fields = ["id", "date", "montant", "mode_paiement", "parent_id"]


class AbsenceSerializer(serializers.ModelSerializer):
    eleve_id = serializers.PrimaryKeyRelatedField(source="eleve", queryset=Eleve.objects.all())
    cours_id = serializers.PrimaryKeyRelatedField(source="cours", queryset=Cours.objects.all())

    class Meta:
        model = Absense
        fields = ["id", "nombre_heure", "date", "nature", "eleve_id", "cours_id"]


# --------------------
# ParentEleve (optionnel si tu gardes la table de jointure explicite)
# --------------------
class ParentEleveSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(source="parent", queryset=Utilisateur.objects.all())
    eleve_id = serializers.PrimaryKeyRelatedField(source="eleve", queryset=Eleve.objects.all())

    class Meta:
        model = ParentEleve
        fields = ["id", "parent_id", "eleve_id"]
