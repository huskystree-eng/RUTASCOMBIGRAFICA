-- Recorrido Lonas P12 · configuración de Supabase
-- 1) Cambia TU_CORREO (abajo, en es_admin) por el correo con el que entrarás como administrador.
-- 2) Pega TODO este archivo en Supabase → SQL Editor → Run.

create table if not exists public.config (
  id int primary key,
  data jsonb not null,
  version bigint not null,
  updated_at timestamptz not null default now()
);

create table if not exists public.avance (
  key text primary key,
  cr text, tienda text, ruta text, marca text, tipo text, medida text,
  estado text not null default '',
  motivo text, nota text, empleado text,
  foto_a text, foto_d text,
  ts_a timestamptz, ts_d timestamptz,
  w_a int, h_a int, w_d int, h_d int,
  updated_at timestamptz not null default now()
);

alter table public.config enable row level security;
alter table public.avance enable row level security;

create or replace function public.es_admin() returns boolean
language sql stable as $$ select lower(coalesce(auth.jwt()->>'email','')) = lower('TU_CORREO') $$;

-- Configuración (rutas, tiendas, piezas): todos leen, solo el administrador escribe
drop policy if exists cfg_read on public.config;
drop policy if exists cfg_ins on public.config;
drop policy if exists cfg_upd on public.config;
create policy cfg_read on public.config for select to anon, authenticated using (true);
create policy cfg_ins  on public.config for insert to authenticated with check (public.es_admin());
create policy cfg_upd  on public.config for update to authenticated using (public.es_admin()) with check (public.es_admin());

-- Avance: los empleados (sin login) lo envían; solo el administrador puede borrar
drop policy if exists av_read on public.avance;
drop policy if exists av_ins on public.avance;
drop policy if exists av_upd on public.avance;
drop policy if exists av_del on public.avance;
create policy av_read on public.avance for select to anon, authenticated using (true);
create policy av_ins  on public.avance for insert to anon, authenticated with check (true);
create policy av_upd  on public.avance for update to anon, authenticated using (true) with check (true);
create policy av_del  on public.avance for delete to authenticated using (public.es_admin());

-- Fotos: carpeta privada. Los empleados solo pueden subir; solo el administrador ve y borra
insert into storage.buckets (id, name, public) values ('fotos', 'fotos', false) on conflict (id) do nothing;
drop policy if exists fotos_ins on storage.objects;
drop policy if exists fotos_sel on storage.objects;
drop policy if exists fotos_del on storage.objects;
create policy fotos_ins on storage.objects for insert to anon, authenticated with check (bucket_id = 'fotos');
create policy fotos_sel on storage.objects for select to authenticated using (bucket_id = 'fotos' and public.es_admin());
create policy fotos_del on storage.objects for delete to authenticated using (bucket_id = 'fotos' and public.es_admin());
