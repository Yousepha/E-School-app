"use client"

import { useEffect, useState } from "react";
import api from "./api";
import toast from "react-hot-toast";

type Matiere = {
  id: string;
  nom: string;
  coef: number;
}

export default function Home() {
  const [matieres, setMatieres] = useState<Matiere[]>([])

  const getMatieres = async () => {
    try {
      const res = await api.get<Matiere[]>("matieres/")
      setMatieres(res.data)
      toast.success("Matières chargées")
    } catch (error) {
      console.error("Erreur chargement matières", error);
      toast.error("Erreur chargement matières")
    }
  }

  useEffect(() => {
    getMatieres()
  }, []);

  return (
    <div className="w-2/3 flex flex-col gap-4">
      <div className="flex justify-between rounded-2xl border-2 border-warning/10 border-dashed bg-warning/5 p-5">
        {matieres.map((matiere) => {
          const nom = matiere.nom;
          const coef = matiere.coef;
          return(
            <div key={matiere.id} className="mb-4">
              <h3>{matiere.nom}  </h3>
              <h3>{matiere.coef}  </h3>
            </div>
          )}

        )}
      </div>
      
    </div>
  );
}
