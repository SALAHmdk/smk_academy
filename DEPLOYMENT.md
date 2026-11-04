# Déploiement — SMK Academy

Hébergeur officiel : **Netlify** (pas de Vercel). Base de données : **Supabase**, projet `smk-academy-dev` (réf. `xebdrfqotzfitbtxeohp`, région eu-west-2).

## 1. Supabase

Migrations (déjà appliquées sur `smk-academy-dev` le 04/11/2026) :

| Fichier | Contenu |
|---|---|
| `20261104090000_init_schema.sql` | tables, RLS, fonctions RPC |
| `20261104091000_seed_python_debutant.sql` | catalogue + formation Python (appliqué en deux parties : catalogue/quiz puis leçons) |
| `20261104092000_harden_grants.sql` | révocation des privilèges par défaut |

Pour régénérer le contenu après modification de `content/python_debutant.py` :

```bash
python3 scripts/build_seed.py > supabase/migrations/<horodatage>_seed_python_debutant.sql
```

Le script est idempotent (UUID déterministes) : il met à jour le contenu sans effacer la progression.

### Réglages Auth à faire dans le tableau de bord Supabase

Authentication > URL Configuration :

- **Site URL** : l'URL Netlify définitive (ex. `https://smk-academy.netlify.app`)
- **Redirect URLs** : `https://smk-academy.netlify.app/**`, `http://localhost:3000/**` et, pour les prévisualisations Netlify, `https://*--smk-academy.netlify.app/**`

Authentication > Emails : le service d'email intégré de Supabase est limité (quelques emails par heure) et réservé aux tests. Avant l'ouverture au public, configurer un SMTP (Resend, Brevo, Postmark…) dans Authentication > SMTP Settings.

## 2. Netlify

Le fichier `netlify.toml` fixe la commande (`npm run build`), le dossier publié (`.next`) et Node 22. L'adaptateur Next.js (OpenNext) est détecté automatiquement.

1. Netlify > Add new project > Import from Git > GitHub > `SALAHmdk/smk_academy`, branche `main`.
2. Variables d'environnement (portée Builds + Functions) :
   - `NEXT_PUBLIC_SUPABASE_URL` = `https://xebdrfqotzfitbtxeohp.supabase.co`
   - `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` = clé `sb_publishable_…` (Supabase > Project Settings > API Keys)
   - `NEXT_PUBLIC_SITE_URL` = URL publique du site
3. Déployer. Toute modification de variable nécessite un nouveau déploiement.
4. Reporter l'URL obtenue dans la configuration Auth de Supabase (section 1).

HTTPS est fourni automatiquement par Netlify. Les prévisualisations de déploiement (Deploy Previews) sont créées pour chaque pull request.

## 3. Paiements Stripe (mode test)

Tant que ces trois variables manquent, la page Tarifs affiche « Paiement en ligne bientôt disponible » ; les codes promo et les accès offerts fonctionnent déjà.

1. **Stripe (mode test)** : Développeurs → Clés API → copier la clé secrète `sk_test_…`.
2. **Webhook Stripe** : Développeurs → Webhooks → Ajouter un endpoint `https://smk-academy.netlify.app/api/webhooks/stripe` avec les événements
   `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed` → copier le secret `whsec_…`.
3. **Jeton base de données** : générer un jeton aléatoire (`openssl rand -hex 32`), puis enregistrer son empreinte dans Supabase (SQL Editor) :
   `insert into private.app_secrets (name, sha256_hex) values ('payments_webhook', encode(extensions.digest('<jeton>', 'sha256'), 'hex')) on conflict (name) do update set sha256_hex = excluded.sha256_hex, updated_at = now();`
4. **Netlify** → Site configuration → Environment variables : `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `PAYMENTS_WEBHOOK_TOKEN` (portée « Functions »), puis redéployer.
5. **Portail client Stripe** : Paramètres → Billing → Portail client → activer (résiliation, moyens de paiement, factures).
6. Moyens de paiement : Paramètres → Moyens de paiement (carte, Apple Pay, Google Pay, Link ; PayPal selon l'éligibilité du compte).

Sécurité : signature Stripe vérifiée (HMAC-SHA256, 5 min), événements réels (`livemode`) refusés par l'application ET par la base, idempotence par identifiant d'événement, prix lus en base uniquement.

## 4. Vérification après déploiement

```bash
E2E_BASE_URL=https://smk-academy.netlify.app E2E_EMAIL=... E2E_PASSWORD=... npm run e2e
```

Puis exécuter `supabase/tests/security_and_grading.sql` dans l'éditeur SQL Supabase : le rapport s'affiche dans le message d'erreur final (toutes les données de test sont annulées).
