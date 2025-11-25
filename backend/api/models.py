from django.db import models
import uuid

# Create your models here.
class Absense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_heure = models.IntegerField()
    date = models.DateField()
    nature = models.CharField(max_length=255)

    eleve = models.ForeignKey("Eleve", on_delete=models.CASCADE)
    cours = models.ForeignKey("Cours", on_delete=models.CASCADE)

    def __str__(self):
        return f"Absence de {self.eleve} le {self.date}"
    
class AnneeScolaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.date_debut.year}-{self.date_fin.year}"
    
class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    nombre_eleve = models.IntegerField()

    def __str__(self):
        return self.nom

class Cours(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    heure_debut = models.CharField(max_length=20)
    heure_fin = models.CharField(max_length=20)
    jour = models.CharField(max_length=20)

    enseignant = models.ForeignKey("Enseignant", on_delete=models.CASCADE)
    matiere = models.ForeignKey("Matiere", on_delete=models.CASCADE)
    classe = models.ForeignKey("Classe", on_delete=models.CASCADE)
    salle = models.ForeignKey("Salle", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.matiere} - {self.jour}"

class Eleve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    photo = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    type_profil = models.CharField(max_length=50)
    numero_eleve = models.IntegerField()

    admin = models.ForeignKey("Utilisateur", on_delete=models.SET_NULL, null=True, related_name="eleves_administres")
    parents = models.ManyToManyField("Utilisateur", related_name="enfants")

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Enseignant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    photo = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    type_profil = models.CharField(max_length=50)
    matricule = models.IntegerField()
    grade = models.CharField(max_length=100)
    date_affiliation = models.DateField()

    admin = models.ForeignKey("Utilisateur", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Inscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    cycle = models.CharField(max_length=50)

    eleve = models.ForeignKey("Eleve", on_delete=models.CASCADE)
    classe = models.ForeignKey("Classe", on_delete=models.CASCADE)
    annee_scolaire = models.ForeignKey("AnneeScolaire", on_delete=models.CASCADE)

    def __str__(self):
        return f"Inscription {self.eleve} - {self.classe}"

class Matiere(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coef = models.FloatField()
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    devoir = models.FloatField()
    composition = models.FloatField()
    examen = models.FloatField()
    semestre = models.CharField(max_length=50)

    matiere = models.ForeignKey("Matiere", on_delete=models.CASCADE)
    eleve = models.ForeignKey("Eleve", on_delete=models.CASCADE)

    def __str__(self):
        return f"Note {self.eleve} - {self.matiere}"

class Paiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    montant = models.IntegerField()
    mode_paiement = models.CharField(max_length=50)

    parent = models.ForeignKey("Utilisateur", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.montant} - {self.parent}"

class ParentEleve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey("Utilisateur", on_delete=models.CASCADE)
    eleve = models.ForeignKey("Eleve", on_delete=models.CASCADE)

class Salle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    capacite = models.IntegerField()

    def __str__(self):
        return self.nom

class Utilisateur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    photo = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    type_profil = models.CharField(max_length=50)

    # enfants → Eleves
    # (déjà dans Eleve.parents)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
