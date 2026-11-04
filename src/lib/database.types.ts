// Généré via Supabase (generate_typescript_types) — schéma public de smk-academy-dev.
// Régénérer après chaque migration modifiant le schéma.

export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[];

export type Database = {
  __InternalSupabase: { PostgrestVersion: "14.18" };
  public: {
    Tables: {
      courses: {
        Row: {
          category: string;
          created_at: string;
          description: string;
          duration_minutes: number;
          id: string;
          is_premium: boolean;
          level: string;
          objectives: string[];
          position: number;
          prerequisites: string[];
          slug: string;
          status: string;
          subtitle: string;
          title: string;
        };
        Insert: never;
        Update: never;
        Relationships: [];
      };
      enrollments: {
        Row: {
          course_id: string;
          created_at: string;
          last_activity_at: string;
          last_lesson_id: string | null;
          user_id: string;
        };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "enrollments_course_id_fkey";
            columns: ["course_id"];
            isOneToOne: false;
            referencedRelation: "courses";
            referencedColumns: ["id"];
          },
          {
            foreignKeyName: "enrollments_last_lesson_id_fkey";
            columns: ["last_lesson_id"];
            isOneToOne: false;
            referencedRelation: "lessons";
            referencedColumns: ["id"];
          },
        ];
      };
      lesson_progress: {
        Row: { completed_at: string; lesson_id: string; user_id: string };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "lesson_progress_lesson_id_fkey";
            columns: ["lesson_id"];
            isOneToOne: false;
            referencedRelation: "lessons";
            referencedColumns: ["id"];
          },
        ];
      };
      lessons: {
        Row: {
          content_md: string;
          duration_minutes: number;
          id: string;
          module_id: string;
          position: number;
          slug: string;
          summary: string;
          title: string;
        };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "lessons_module_id_fkey";
            columns: ["module_id"];
            isOneToOne: false;
            referencedRelation: "modules";
            referencedColumns: ["id"];
          },
        ];
      };
      modules: {
        Row: { course_id: string; description: string; id: string; position: number; status: string; title: string };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "modules_course_id_fkey";
            columns: ["course_id"];
            isOneToOne: false;
            referencedRelation: "courses";
            referencedColumns: ["id"];
          },
        ];
      };
      profiles: {
        Row: { created_at: string; full_name: string; id: string; plan: string; role: string; updated_at: string };
        Insert: never;
        Update: { full_name?: string };
        Relationships: [];
      };
      quiz_attempts: {
        Row: {
          corrections: Json;
          created_at: string;
          id: string;
          max_points: number;
          passed: boolean;
          points: number;
          quiz_id: string;
          score_20: number;
          user_id: string;
        };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "quiz_attempts_quiz_id_fkey";
            columns: ["quiz_id"];
            isOneToOne: false;
            referencedRelation: "quizzes";
            referencedColumns: ["id"];
          },
        ];
      };
      quiz_options: {
        Row: { id: string; label: string; position: number; question_id: string };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "quiz_options_question_id_fkey";
            columns: ["question_id"];
            isOneToOne: false;
            referencedRelation: "quiz_questions";
            referencedColumns: ["id"];
          },
        ];
      };
      quiz_questions: {
        Row: {
          code: string | null;
          id: string;
          kind: string;
          points: number;
          position: number;
          prompt: string;
          quiz_id: string;
        };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "quiz_questions_quiz_id_fkey";
            columns: ["quiz_id"];
            isOneToOne: false;
            referencedRelation: "quizzes";
            referencedColumns: ["id"];
          },
        ];
      };
      quizzes: {
        Row: { id: string; module_id: string; pass_mark: number; title: string };
        Insert: never;
        Update: never;
        Relationships: [
          {
            foreignKeyName: "quizzes_module_id_fkey";
            columns: ["module_id"];
            isOneToOne: true;
            referencedRelation: "modules";
            referencedColumns: ["id"];
          },
        ];
      };
    };
    Views: { [_ in never]: never };
    Functions: {
      complete_lesson: { Args: { p_lesson_id: string }; Returns: undefined };
      enroll_in_course: { Args: { p_course_id: string }; Returns: undefined };
      submit_quiz: {
        Args: { p_answers: Json; p_quiz_id: string };
        Returns: Database["public"]["Tables"]["quiz_attempts"]["Row"];
        SetofOptions: { from: "*"; to: "quiz_attempts"; isOneToOne: true; isSetofReturn: false };
      };
      touch_lesson: { Args: { p_lesson_id: string }; Returns: undefined };
    };
    Enums: { [_ in never]: never };
    CompositeTypes: { [_ in never]: never };
  };
};

