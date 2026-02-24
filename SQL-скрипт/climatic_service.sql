--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2026-02-24 19:18:10

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

--
-- TOC entry 218 (class 1259 OID 33040)
-- Name: climate_tech_types_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.climate_tech_types_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.climate_tech_types_type_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 33054)
-- Name: climate_tech_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.climate_tech_types (
    type_id integer DEFAULT nextval('public.climate_tech_types_type_id_seq'::regclass) NOT NULL,
    type_name character varying(50) NOT NULL,
    type_description text
);


ALTER TABLE public.climate_tech_types OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 33043)
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comments_comment_id_seq
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_comment_id_seq OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 33109)
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comments (
    comment_id integer DEFAULT nextval('public.comments_comment_id_seq'::regclass) NOT NULL,
    message text NOT NULL,
    master_id integer NOT NULL,
    request_id integer NOT NULL
);


ALTER TABLE public.comments OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 33041)
-- Name: request_statuses_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.request_statuses_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.request_statuses_status_id_seq OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 33064)
-- Name: request_statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.request_statuses (
    status_id integer DEFAULT nextval('public.request_statuses_status_id_seq'::regclass) NOT NULL,
    status_name character varying(50) NOT NULL,
    status_description text
);


ALTER TABLE public.request_statuses OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 33042)
-- Name: requests_request_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requests_request_id_seq
    START WITH 6
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.requests_request_id_seq OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 33074)
-- Name: requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requests (
    request_id integer DEFAULT nextval('public.requests_request_id_seq'::regclass) NOT NULL,
    start_date date NOT NULL,
    type_id integer NOT NULL,
    model character varying(100) NOT NULL,
    problem_description text NOT NULL,
    status_id integer NOT NULL,
    completion_date date,
    repair_parts text,
    master_id integer,
    client_id integer NOT NULL,
    quality_manager_id integer,
    deadline_extended boolean DEFAULT false,
    CONSTRAINT check_dates CHECK (((completion_date IS NULL) OR (completion_date >= start_date)))
);


ALTER TABLE public.requests OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 33039)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 33044)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer DEFAULT nextval('public.users_user_id_seq'::regclass) NOT NULL,
    fio character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    login character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    type character varying(20) NOT NULL,
    is_deleted boolean DEFAULT false,
    CONSTRAINT users_type_check CHECK (((type)::text = ANY ((ARRAY['Менеджер'::character varying, 'Специалист'::character varying, 'Оператор'::character varying, 'Заказчик'::character varying, 'Менеджер по качеству'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 4850 (class 0 OID 33054)
-- Dependencies: 223
-- Data for Name: climate_tech_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.climate_tech_types VALUES (1, 'Кондиционер', NULL);
INSERT INTO public.climate_tech_types VALUES (2, 'Увлажнитель воздуха', NULL);
INSERT INTO public.climate_tech_types VALUES (3, 'Сушилка для рук', NULL);


--
-- TOC entry 4853 (class 0 OID 33109)
-- Dependencies: 226
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.comments VALUES (1, 'Всё сделаем!', 2, 1);
INSERT INTO public.comments VALUES (2, 'Всё сделаем!', 3, 2);
INSERT INTO public.comments VALUES (3, 'Починим в момент.', 3, 3);


--
-- TOC entry 4851 (class 0 OID 33064)
-- Dependencies: 224
-- Data for Name: request_statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.request_statuses VALUES (1, 'Новая заявка', NULL);
INSERT INTO public.request_statuses VALUES (2, 'В процессе ремонта', NULL);
INSERT INTO public.request_statuses VALUES (3, 'Готова к выдаче', NULL);
INSERT INTO public.request_statuses VALUES (4, 'Ожидание комплектующих', NULL);
INSERT INTO public.request_statuses VALUES (5, 'Завершена', NULL);
INSERT INTO public.request_statuses VALUES (6, 'Просрочена', NULL);


--
-- TOC entry 4852 (class 0 OID 33074)
-- Dependencies: 225
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.requests VALUES (1, '2023-06-06', 1, 'TCL TAC-12CHSA/TPG-W белый', 'Не охлаждает воздух', 2, NULL, NULL, 2, 7, NULL, false);
INSERT INTO public.requests VALUES (2, '2023-05-05', 1, 'Electrolux EACS/I-09HAT/N3_21Y белый', 'Выключается сам по себе', 2, NULL, NULL, 3, 8, NULL, false);
INSERT INTO public.requests VALUES (3, '2022-07-07', 2, 'Xiaomi Smart Humidifier 2', 'Пар имеет неприятный запах', 3, '2023-01-01', NULL, 3, 9, NULL, false);
INSERT INTO public.requests VALUES (4, '2023-08-02', 2, 'Polaris PUH 2300 WIFI IQ Home', 'Увлажнитель воздуха продолжает работать при предельном снижении уровня воды', 1, NULL, NULL, NULL, 8, NULL, false);
INSERT INTO public.requests VALUES (5, '2023-08-02', 3, 'Ballu BAHD-1250', 'Не работает', 1, NULL, NULL, NULL, 9, NULL, false);


--
-- TOC entry 4849 (class 0 OID 33044)
-- Dependencies: 222
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, 'Широков Василий Матвеевич', '89210563128', 'login1', 'pass1', 'Менеджер', false);
INSERT INTO public.users VALUES (2, 'Кудрявцева Ева Ивановна', '89535078985', 'login2', 'pass2', 'Специалист', false);
INSERT INTO public.users VALUES (3, 'Гончарова Ульяна Ярославовна', '89210673849', 'login3', 'pass3', 'Специалист', false);
INSERT INTO public.users VALUES (4, 'Гусева Виктория Данииловна', '89990563748', 'login4', 'pass4', 'Оператор', false);
INSERT INTO public.users VALUES (5, 'Баранов Артём Юрьевич', '89994563847', 'login5', 'pass5', 'Оператор', false);
INSERT INTO public.users VALUES (6, 'Овчинников Фёдор Никитич', '89219567849', 'login6', 'pass6', 'Заказчик', false);
INSERT INTO public.users VALUES (7, 'Петров Никита Артёмович', '89219567841', 'login7', 'pass7', 'Заказчик', false);
INSERT INTO public.users VALUES (8, 'Ковалева Софья Владимировна', '89219567842', 'login8', 'pass8', 'Заказчик', false);
INSERT INTO public.users VALUES (9, 'Кузнецов Сергей Матвеевич', '89219567843', 'login9', 'pass9', 'Заказчик', false);
INSERT INTO public.users VALUES (10, 'Беспалова Екатерина Даниэльевна', '89219567844', 'login10', 'pass10', 'Специалист', false);


--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 218
-- Name: climate_tech_types_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.climate_tech_types_type_id_seq', 1, false);


--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 221
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 3, true);


--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 219
-- Name: request_statuses_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.request_statuses_status_id_seq', 1, false);


--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 220
-- Name: requests_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requests_request_id_seq', 5, true);


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 10, true);


--
-- TOC entry 4675 (class 2606 OID 33061)
-- Name: climate_tech_types climate_tech_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.climate_tech_types
    ADD CONSTRAINT climate_tech_types_pkey PRIMARY KEY (type_id);


--
-- TOC entry 4677 (class 2606 OID 33063)
-- Name: climate_tech_types climate_tech_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.climate_tech_types
    ADD CONSTRAINT climate_tech_types_type_name_key UNIQUE (type_name);


--
-- TOC entry 4690 (class 2606 OID 33116)
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- TOC entry 4679 (class 2606 OID 33071)
-- Name: request_statuses request_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_statuses
    ADD CONSTRAINT request_statuses_pkey PRIMARY KEY (status_id);


--
-- TOC entry 4681 (class 2606 OID 33073)
-- Name: request_statuses request_statuses_status_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_statuses
    ADD CONSTRAINT request_statuses_status_name_key UNIQUE (status_name);


--
-- TOC entry 4688 (class 2606 OID 33083)
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (request_id);


--
-- TOC entry 4671 (class 2606 OID 33053)
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- TOC entry 4673 (class 2606 OID 33051)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4691 (class 1259 OID 33132)
-- Name: idx_comments_request; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_comments_request ON public.comments USING btree (request_id);


--
-- TOC entry 4682 (class 1259 OID 33127)
-- Name: idx_requests_client; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_requests_client ON public.requests USING btree (client_id);


--
-- TOC entry 4683 (class 1259 OID 33128)
-- Name: idx_requests_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_requests_master ON public.requests USING btree (master_id);


--
-- TOC entry 4684 (class 1259 OID 33131)
-- Name: idx_requests_start_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_requests_start_date ON public.requests USING btree (start_date);


--
-- TOC entry 4685 (class 1259 OID 33129)
-- Name: idx_requests_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_requests_status ON public.requests USING btree (status_id);


--
-- TOC entry 4686 (class 1259 OID 33130)
-- Name: idx_requests_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_requests_type ON public.requests USING btree (type_id);


--
-- TOC entry 4697 (class 2606 OID 33117)
-- Name: comments fk_comments_master; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT fk_comments_master FOREIGN KEY (master_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 4698 (class 2606 OID 33122)
-- Name: comments fk_comments_request; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT fk_comments_request FOREIGN KEY (request_id) REFERENCES public.requests(request_id) ON DELETE CASCADE;


--
-- TOC entry 4692 (class 2606 OID 33099)
-- Name: requests fk_requests_client; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_client FOREIGN KEY (client_id) REFERENCES public.users(user_id) ON DELETE RESTRICT;


--
-- TOC entry 4693 (class 2606 OID 33094)
-- Name: requests fk_requests_master; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_master FOREIGN KEY (master_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 4694 (class 2606 OID 33104)
-- Name: requests fk_requests_quality_manager; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_quality_manager FOREIGN KEY (quality_manager_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 4695 (class 2606 OID 33089)
-- Name: requests fk_requests_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_status FOREIGN KEY (status_id) REFERENCES public.request_statuses(status_id) ON DELETE RESTRICT;


--
-- TOC entry 4696 (class 2606 OID 33084)
-- Name: requests fk_requests_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_type FOREIGN KEY (type_id) REFERENCES public.climate_tech_types(type_id) ON DELETE RESTRICT;


-- Completed on 2026-02-24 19:18:15

--
-- PostgreSQL database dump complete
--

