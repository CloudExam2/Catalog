--
-- PostgreSQL database dump
--

\restrict 7tXQPJBP3tQKUA6UgxorsTgW4pjL0ZjivCitsGKWdnfyWXDiJoqXaLaJpZcriEw

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: addresses; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.addresses (
    id integer NOT NULL,
    domicilio text NOT NULL,
    colonia character varying(100),
    municipio character varying(100),
    estado character varying(100),
    address_type character varying(20)
);


ALTER TABLE public.addresses OWNER TO admin;

--
-- Name: addresses_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.addresses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.addresses_id_seq OWNER TO admin;

--
-- Name: addresses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.addresses_id_seq OWNED BY public.addresses.id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.clients (
    id integer NOT NULL,
    rfc character varying(13) NOT NULL,
    razon_social character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    comercial_name character varying(255),
    telefono character varying(20)
);


ALTER TABLE public.clients OWNER TO admin;

--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.clients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_id_seq OWNER TO admin;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.clients_id_seq OWNED BY public.clients.id;


--
-- Name: notecontent; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.notecontent (
    id integer NOT NULL,
    note_id integer,
    product_id integer,
    unit_price numeric(10,2) NOT NULL,
    quantity integer NOT NULL,
    total numeric(10,2) NOT NULL
);


ALTER TABLE public.notecontent OWNER TO admin;

--
-- Name: notecontent_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.notecontent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notecontent_id_seq OWNER TO admin;

--
-- Name: notecontent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.notecontent_id_seq OWNED BY public.notecontent.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    unit character varying(50),
    base_price numeric(10,2) NOT NULL
);


ALTER TABLE public.products OWNER TO admin;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO admin;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: salesnotes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.salesnotes (
    id integer NOT NULL,
    folio character varying(50) NOT NULL,
    client_id integer,
    fac_address_id integer,
    send_address_id integer,
    total numeric(10,2) DEFAULT 0.00
);


ALTER TABLE public.salesnotes OWNER TO admin;

--
-- Name: salesnotes_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.salesnotes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.salesnotes_id_seq OWNER TO admin;

--
-- Name: salesnotes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.salesnotes_id_seq OWNED BY public.salesnotes.id;


--
-- Name: addresses id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.addresses ALTER COLUMN id SET DEFAULT nextval('public.addresses_id_seq'::regclass);


--
-- Name: clients id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id_seq'::regclass);


--
-- Name: notecontent id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notecontent ALTER COLUMN id SET DEFAULT nextval('public.notecontent_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: salesnotes id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.salesnotes ALTER COLUMN id SET DEFAULT nextval('public.salesnotes_id_seq'::regclass);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: clients clients_rfc_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_rfc_key UNIQUE (rfc);


--
-- Name: notecontent notecontent_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notecontent
    ADD CONSTRAINT notecontent_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: salesnotes salesnotes_folio_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.salesnotes
    ADD CONSTRAINT salesnotes_folio_key UNIQUE (folio);


--
-- Name: salesnotes salesnotes_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.salesnotes
    ADD CONSTRAINT salesnotes_pkey PRIMARY KEY (id);


--
-- Name: notecontent notecontent_note_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notecontent
    ADD CONSTRAINT notecontent_note_id_fkey FOREIGN KEY (note_id) REFERENCES public.salesnotes(id);


--
-- Name: notecontent notecontent_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.notecontent
    ADD CONSTRAINT notecontent_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: salesnotes salesnotes_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.salesnotes
    ADD CONSTRAINT salesnotes_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: salesnotes salesnotes_fac_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.salesnotes
    ADD CONSTRAINT salesnotes_fac_address_id_fkey FOREIGN KEY (fac_address_id) REFERENCES public.addresses(id);


--
-- Name: salesnotes salesnotes_send_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.salesnotes
    ADD CONSTRAINT salesnotes_send_address_id_fkey FOREIGN KEY (send_address_id) REFERENCES public.addresses(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 7tXQPJBP3tQKUA6UgxorsTgW4pjL0ZjivCitsGKWdnfyWXDiJoqXaLaJpZcriEw

