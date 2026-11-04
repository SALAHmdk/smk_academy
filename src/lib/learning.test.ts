import { describe, expect, it } from "vitest";
import {
  answersFromFormData,
  averageOfBest,
  filterCatalog,
  formatDuration,
  formatScore,
  orderLessons,
  percent,
  quizSubmissionSchema,
  safeNextPath,
} from "./learning";

const Q1 = "4d482a46-cdc9-5a2d-af30-f6697f046f49";
const O1 = "0c58d56f-7000-559d-ab48-8f3c1d7b1530";
const O2 = "69a6177c-7d2b-5855-aa10-c7f9b128d95c";

describe("formatage", () => {
  it("formate les durées", () => {
    expect(formatDuration(45)).toBe("45 min");
    expect(formatDuration(60)).toBe("1 h");
    expect(formatDuration(605)).toBe("10 h 05");
  });

  it("formate les notes à la française", () => {
    expect(formatScore(17.5)).toBe("17,5");
    expect(formatScore(20)).toBe("20");
    expect(formatScore(13.333)).toBe("13,33");
  });

  it("calcule un pourcentage borné", () => {
    expect(percent(0, 0)).toBe(0);
    expect(percent(3, 6)).toBe(50);
    expect(percent(7, 6)).toBe(100);
  });
});

describe("moyenne des meilleures notes", () => {
  it("retient la meilleure tentative par quiz", () => {
    expect(
      averageOfBest([
        { quiz_id: "a", score_20: 8 },
        { quiz_id: "a", score_20: 16 },
        { quiz_id: "b", score_20: 12 },
      ]),
    ).toBe(14);
  });
  it("renvoie null sans tentative", () => {
    expect(averageOfBest([])).toBeNull();
  });
});

describe("ordre des leçons", () => {
  it("trie par module puis par position", () => {
    const modules = [
      { id: "m2", position: 2 },
      { id: "m1", position: 1 },
    ];
    const lessons = [
      { id: "b", module_id: "m2", position: 1 },
      { id: "a2", module_id: "m1", position: 2 },
      { id: "a1", module_id: "m1", position: 1 },
      { id: "x", module_id: "inconnu", position: 1 },
    ];
    expect(orderLessons(modules, lessons).map((l) => l.id)).toEqual(["a1", "a2", "b"]);
  });
});

describe("soumission de quiz", () => {
  it("regroupe les réponses du formulaire par question", () => {
    const form = new FormData();
    form.append("quizId", "ignored");
    form.append(`q_${Q1}`, O1);
    form.append(`q_${Q1}`, O2);
    expect(answersFromFormData(form)).toEqual({ [Q1]: [O1, O2] });
  });

  it("accepte une soumission valide", () => {
    const r = quizSubmissionSchema.safeParse({ quizId: Q1, answers: { [Q1]: [O1] } });
    expect(r.success).toBe(true);
  });

  it("rejette des identifiants forgés", () => {
    expect(quizSubmissionSchema.safeParse({ quizId: "1; drop table", answers: {} }).success).toBe(false);
    expect(quizSubmissionSchema.safeParse({ quizId: Q1, answers: { x: [O1] } }).success).toBe(false);
    expect(quizSubmissionSchema.safeParse({ quizId: Q1, answers: { [Q1]: ["' or 1=1"] } }).success).toBe(false);
  });
});

describe("redirections", () => {
  it("garde les chemins internes", () => {
    expect(safeNextPath("/formations/python-debutant")).toBe("/formations/python-debutant");
  });
  it("refuse les redirections externes", () => {
    expect(safeNextPath("https://evil.example")).toBe("/tableau-de-bord");
    expect(safeNextPath("//evil.example")).toBe("/tableau-de-bord");
    expect(safeNextPath("/\\evil.example")).toBe("/tableau-de-bord");
    expect(safeNextPath(null)).toBe("/tableau-de-bord");
  });
});

describe("filtres du catalogue", () => {
  const base = {
    id: "x", subtitle: "", description: "", category_id: "c", cover_label: "", duration_minutes: 60,
    objectives: [], prerequisites: [], is_premium: false, position: 1,
  };
  const courses = [
    { ...base, slug: "python", title: "Python pour débutants", topic: "Python", level: "debutant", status: "published", categories: { slug: "programmation", name: "Programmation" } },
    { ...base, slug: "sql", title: "SQL pour débutants", topic: "SQL", level: "debutant", status: "coming_soon", categories: { slug: "bases-de-donnees", name: "Bases de données" } },
    { ...base, slug: "k8s", title: "Kubernetes", topic: "Kubernetes", level: "avance", status: "coming_soon", categories: { slug: "cloud-devops", name: "Cloud et DevOps" } },
  ] as unknown as import("./learning").Course[];

  it("recherche sans tenir compte des accents ni de la casse", () => {
    expect(filterCatalog(courses, { q: "DEBUTANTS" }).map((c) => c.slug)).toEqual(["python", "sql"]);
    expect(filterCatalog(courses, { q: "données" }).map((c) => c.slug)).toEqual(["sql"]);
  });
  it("filtre par catégorie, langage, niveau et disponibilité", () => {
    expect(filterCatalog(courses, { categorie: "cloud-devops" }).map((c) => c.slug)).toEqual(["k8s"]);
    expect(filterCatalog(courses, { langage: "SQL" }).map((c) => c.slug)).toEqual(["sql"]);
    expect(filterCatalog(courses, { niveau: "avance" }).map((c) => c.slug)).toEqual(["k8s"]);
    expect(filterCatalog(courses, { dispo: "1" }).map((c) => c.slug)).toEqual(["python"]);
  });
});
