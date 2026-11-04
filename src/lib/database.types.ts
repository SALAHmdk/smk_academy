// Généré via Supabase (generate_typescript_types) — schéma public de smk-academy-dev.
// Régénérer après chaque migration modifiant le schéma.

export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[];

export type Database = {
  __InternalSupabase: { PostgrestVersion: "14.18" };
  public: {
    Tables: {
      categories: {
        Row: { created_at: string; description: string; id: string; name: string; position: number; slug: string };
        Insert: { created_at?: string; description?: string; id?: string; name: string; position?: number; slug: string };
        Update: { created_at?: string; description?: string; id?: string; name?: string; position?: number; slug?: string };
        Relationships: [];
      };
      courses: {
        Row: {
          category_id: string;
          cover_label: string;
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
          topic: string;
          updated_at: string;
        };
        Insert: {
          category_id: string;
          cover_label?: string;
          created_at?: string;
          description?: string;
          duration_minutes?: number;
          id?: string;
          is_premium?: boolean;
          level: string;
          objectives?: string[];
          position?: number;
          prerequisites?: string[];
          slug: string;
          status?: string;
          subtitle?: string;
          title: string;
          topic?: string;
          updated_at?: string;
        };
        Update: {
          category_id?: string;
          cover_label?: string;
          created_at?: string;
          description?: string;
          duration_minutes?: number;
          id?: string;
          is_premium?: boolean;
          level?: string;
          objectives?: string[];
          position?: number;
          prerequisites?: string[];
          slug?: string;
          status?: string;
          subtitle?: string;
          title?: string;
          topic?: string;
          updated_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: "courses_category_id_fkey";
            columns: ["category_id"];
            isOneToOne: false;
            referencedRelation: "categories";
            referencedColumns: ["id"];
          },
        ];
      };
      enrollments: {
        Row: { course_id: string; created_at: string; last_activity_at: string; last_lesson_id: string | null; user_id: string };
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
        Insert: {
          content_md: string;
          duration_minutes?: number;
          id?: string;
          module_id: string;
          position: number;
          slug: string;
          summary?: string;
          title: string;
        };
        Update: {
          content_md?: string;
          duration_minutes?: number;
          id?: string;
          module_id?: string;
          position?: number;
          slug?: string;
          summary?: string;
          title?: string;
        };
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
        Insert: { course_id: string; description?: string; id?: string; position: number; status?: string; title: string };
        Update: { course_id?: string; description?: string; id?: string; position?: number; status?: string; title?: string };
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
      payments: {
        Row: {
          amount_cents: number;
          created_at: string;
          currency: string;
          id: string;
          livemode: boolean;
          plan_id: string | null;
          provider: string;
          provider_ref: string;
          provider_subscription_id: string | null;
          status: string;
          user_id: string | null;
        };
        Insert: never;
        Update: never;
        Relationships: [];
      };
      plans: {
        Row: {
          billing_interval: string | null;
          currency: string;
          features: string[];
          id: string;
          is_active: boolean;
          name: string;
          position: number;
          price_cents: number;
          tagline: string;
          updated_at: string;
        };
        Insert: never;
        Update: { name?: string; tagline?: string; price_cents?: number; features?: string[]; is_active?: boolean };
        Relationships: [];
      };
      premium_grants: {
        Row: {
          created_at: string;
          ends_at: string | null;
          granted_by: string | null;
          id: string;
          note: string;
          promo_code_id: string | null;
          revoked_at: string | null;
          source: string;
          starts_at: string;
          user_id: string;
        };
        Insert: never;
        Update: never;
        Relationships: [];
      };
      promo_codes: {
        Row: {
          code: string;
          created_at: string;
          created_by: string | null;
          disabled_at: string | null;
          expires_at: string | null;
          id: string;
          max_redemptions: number;
          months: number | null;
          note: string;
          redemptions_count: number;
          restricted_email: string | null;
        };
        Insert: never;
        Update: never;
        Relationships: [];
      };
      promo_redemptions: {
        Row: { grant_id: string | null; id: string; promo_code_id: string; redeemed_at: string; user_id: string };
        Insert: never;
        Update: never;
        Relationships: [];
      };
      subscriptions: {
        Row: {
          cancel_at_period_end: boolean;
          created_at: string;
          current_period_end: string | null;
          id: string;
          plan_id: string | null;
          provider: string;
          provider_customer_id: string | null;
          provider_subscription_id: string;
          status: string;
          updated_at: string;
          user_id: string;
        };
        Insert: never;
        Update: never;
        Relationships: [];
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
        Insert: { id?: string; label: string; position: number; question_id: string };
        Update: { id?: string; label?: string; position?: number; question_id?: string };
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
        Row: { code: string | null; id: string; kind: string; points: number; position: number; prompt: string; quiz_id: string };
        Insert: {
          code?: string | null;
          id?: string;
          kind: string;
          points?: number;
          position: number;
          prompt: string;
          quiz_id: string;
        };
        Update: {
          code?: string | null;
          id?: string;
          kind?: string;
          points?: number;
          position?: number;
          prompt?: string;
          quiz_id?: string;
        };
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
        Insert: { id?: string; module_id: string; pass_mark?: number; title: string };
        Update: { id?: string; module_id?: string; pass_mark?: number; title?: string };
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
      admin_audit_log: {
        Args: { p_limit?: number };
        Returns: { action: string; actor_email: string; at: string; entity: string; entity_id: string; summary: Json }[];
      };
      admin_get_answer_keys: {
        Args: { p_quiz_id: string };
        Returns: { correct_option_ids: string[]; explanation: string; question_id: string }[];
      };
      admin_set_answer_key: {
        Args: { p_correct: string[]; p_explanation: string; p_question_id: string };
        Returns: undefined;
      };
      admin_stats: { Args: never; Returns: Json };
      admin_create_promo_code: {
        Args: {
          p_code?: string;
          p_expires_at: string | null;
          p_max_redemptions: number;
          p_months: number | null;
          p_note: string;
          p_restricted_email: string | null;
        };
        Returns: string;
      };
      admin_disable_promo_code: { Args: { p_id: string }; Returns: undefined };
      admin_grant_premium: { Args: { p_email: string; p_months: number | null; p_note: string }; Returns: string };
      admin_payments_overview: { Args: never; Returns: Json };
      admin_premium_members: {
        Args: never;
        Returns: {
          created_at: string;
          email: string;
          ends_at: string | null;
          grant_id: string;
          note: string;
          revoked_at: string | null;
          source: string;
          starts_at: string;
        }[];
      };
      admin_revoke_premium: { Args: { p_grant_id: string }; Returns: undefined };
      my_access: { Args: never; Returns: Json };
      payments_apply_event: {
        Args: { p_data: Json; p_event_id: string; p_provider: string; p_token: string; p_type: string };
        Returns: string;
      };
      redeem_promo_code: { Args: { p_code: string }; Returns: Json };
      complete_lesson: { Args: { p_lesson_id: string }; Returns: undefined };
      enroll_in_course: { Args: { p_course_id: string }; Returns: undefined };
      my_role: { Args: never; Returns: string };
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
