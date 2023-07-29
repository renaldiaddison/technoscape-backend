--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

-- Started on 2023-07-29 19:52:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3457 (class 0 OID 18699)
-- Dependencies: 216
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 3453 (class 0 OID 18685)
-- Dependencies: 212
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	user	userapproval
8	user	user
9	loan	loanapproval
10	loan	loan
11	loan	loanhistory
12	loan	loanapprovalhistory
13	forgot_password_link	forgotpasswordlink
\.


--
-- TOC entry 3455 (class 0 OID 18693)
-- Dependencies: 214
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add user approval	7	add_userapproval
26	Can change user approval	7	change_userapproval
27	Can delete user approval	7	delete_userapproval
28	Can view user approval	7	view_userapproval
29	Can add user	8	add_user
30	Can change user	8	change_user
31	Can delete user	8	delete_user
32	Can view user	8	view_user
33	Can add loan approval	9	add_loanapproval
34	Can change loan approval	9	change_loanapproval
35	Can delete loan approval	9	delete_loanapproval
36	Can view loan approval	9	view_loanapproval
37	Can add loan	10	add_loan
38	Can change loan	10	change_loan
39	Can delete loan	10	delete_loan
40	Can view loan	10	view_loan
41	Can add loan history	11	add_loanhistory
42	Can change loan history	11	change_loanhistory
43	Can delete loan history	11	delete_loanhistory
44	Can view loan history	11	view_loanhistory
45	Can add loan approval history	12	add_loanapprovalhistory
46	Can change loan approval history	12	change_loanapprovalhistory
47	Can delete loan approval history	12	delete_loanapprovalhistory
48	Can view loan approval history	12	view_loanapprovalhistory
49	Can add forgot password link	13	add_forgotpasswordlink
50	Can change forgot password link	13	change_forgotpasswordlink
51	Can delete forgot password link	13	delete_forgotpasswordlink
52	Can view forgot password link	13	view_forgotpasswordlink
\.


--
-- TOC entry 3459 (class 0 OID 18707)
-- Dependencies: 218
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 3461 (class 0 OID 18713)
-- Dependencies: 220
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- TOC entry 3463 (class 0 OID 18721)
-- Dependencies: 222
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 3465 (class 0 OID 18727)
-- Dependencies: 224
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 3467 (class 0 OID 18785)
-- Dependencies: 226
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 3451 (class 0 OID 18677)
-- Dependencies: 210
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2023-07-28 19:49:37.394142+07
2	auth	0001_initial	2023-07-28 19:49:37.485086+07
3	admin	0001_initial	2023-07-28 19:49:37.510015+07
4	admin	0002_logentry_remove_auto_add	2023-07-28 19:49:37.51553+07
5	admin	0003_logentry_add_action_flag_choices	2023-07-28 19:49:37.522704+07
6	contenttypes	0002_remove_content_type_name	2023-07-28 19:49:37.536347+07
7	auth	0002_alter_permission_name_max_length	2023-07-28 19:49:37.542512+07
8	auth	0003_alter_user_email_max_length	2023-07-28 19:49:37.548909+07
9	auth	0004_alter_user_username_opts	2023-07-28 19:49:37.555202+07
10	auth	0005_alter_user_last_login_null	2023-07-28 19:49:37.56167+07
11	auth	0006_require_contenttypes_0002	2023-07-28 19:49:37.563889+07
12	auth	0007_alter_validators_add_error_messages	2023-07-28 19:49:37.568887+07
13	auth	0008_alter_user_username_max_length	2023-07-28 19:49:37.582662+07
14	auth	0009_alter_user_last_name_max_length	2023-07-28 19:49:37.588672+07
15	auth	0010_alter_group_name_max_length	2023-07-28 19:49:37.595671+07
16	auth	0011_update_proxy_permissions	2023-07-28 19:49:37.602955+07
17	auth	0012_alter_user_first_name_max_length	2023-07-28 19:49:37.609007+07
18	sessions	0001_initial	2023-07-28 19:49:37.623298+07
19	user	0001_initial	2023-07-28 19:49:37.655443+07
20	loan	0001_initial	2023-07-28 21:14:44.051882+07
21	loan	0002_loanapproval_created_at	2023-07-28 21:46:54.087263+07
22	user	0002_user_gender	2023-07-28 21:46:54.092812+07
23	user	0003_userapproval_credit_history	2023-07-28 21:57:42.884755+07
24	user	0004_alter_userapproval_credit_history	2023-07-28 21:57:56.66332+07
25	loan	0003_loanapproval_rate_alter_loanapproval_is_approved_and_more	2023-07-29 00:00:14.256878+07
26	forgot_password_link	0001_initial	2023-07-29 01:22:54.413403+07
27	loan	0004_loan_created_at_loanhistory_created_at	2023-07-29 09:39:56.483138+07
28	loan	0005_remove_loanhistory_approval_loanapproval_is_done_and_more	2023-07-29 09:39:56.507402+07
29	loan	0006_alter_loanapproval_is_done	2023-07-29 12:59:59.775166+07
30	user	0005_user_account_no	2023-07-29 15:42:33.743283+07
\.


--
-- TOC entry 3468 (class 0 OID 18813)
-- Dependencies: 227
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- TOC entry 3470 (class 0 OID 18823)
-- Dependencies: 229
-- Data for Name: user_approvals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_approvals (id, married, dependent, education, self_employed, income, coappliciant_income, property_area, credit_history) FROM stdin;
1	1	3	0	1	123123	123123	1	1
2	1	3	0	1	123123	123123	1	1
3	0	3	0	1	123	123	1	1
4	1	3	0	1	123	123	1	1
5	1	1	0	1	123123	213414	2	1
6	0	1	1	1	2000	2000	2	1
7	1	2	1	0	3000	2000	1	1
8	1	3	0	1	0	0	1	0
10	1	3	1	0	2000	3000	2	1
11	1	2	1	0	3000	4000	2	1
12	1	3	1	1	2000	3000	2	1
9	1	3	0	1	13000000	20000000	1	1
13	0	4	0	1	1000000	2020200	1	1
14	1	3	0	1	200000	60000	2	1
15	1	3	1	1	30000000	3000000	2	1
16	1	3	1	1	300000	25000	2	1
17	0	3	1	1	1000000	1200000	2	1
18	0	3	0	1	12313212321	1232132123	2	1
\.


--
-- TOC entry 3472 (class 0 OID 18829)
-- Dependencies: 231
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (uid, username, email, old_password, current_password, is_approved, pin, role, user_approval_id, gender, account_no) FROM stdin;
264	kakaka	kakaka@gmail.com	kakaka123	kakaka123	f	123456	USER	\N	1	5859452642402327
123	meja	meja@gmail.com	meja123	meja123	f	1123	USER	\N	0	5859458470782741
111	jaja	jaja@gmail.com	asd123	asd123	t	123456	ADMIN	5	0	5859455512376902
134	gelas	gelas@gmail.com	gelas123	gelas123	t	12312	USER	6	1	5859456171837164
142	JD22-1	jd@gmail.com	221	221	t	221221	USER	8	1	5859457924141316
125	re221	re@gmail.com	221	221	t	132421	USER	9	0	5859457287248296
179	pintu	pintu@gmail.com	pintu123	pintu123	t	1234	USER	10	1	5859456886680633
183	mneach	mneachdev@gmail.com	mneach	halo123	t	121212	USER	11	1	5859452835687966
196	aduy	muhamad.fitrayuda@gmail.com	aduy	aduy123	t	102941	USER	12	1	5859457310078804
266	huhu	huhu@gmail.com	huhu123	huhu123	t	123456	USER	13	1	5859458120290690
346	Renaldy	muhamad.learning@gmail.com	renaldy123	renaldy123	f	123456	USER	\N	1	5859452512792007
348	kerupuk	kerupuk@gmail.com	keurpuk123	keurpuk123	f	123456	USER	\N	1	5859452279421885
349	tester1234	mneach.gaming@gmail.com	tester1234	tester1234	t	123456	USER	14	1	5859453815375927
359	titi	titi@gmail.com	titi123	titi123	t	123456	USER	15	1	5859453107378195
361	lala	lala@gmail.com	lala123	lala123	t	123456	USER	16	1	5859458105403654
366	bluejack	bluejackslc221@gmail.com	bluejack123	bluejack321	t	123456	USER	17	1	5859454508081710
368	baru	baru@gmail.com	baru123	baru123	t	123456	USER	18	1	5859459313519573
\.


--
-- TOC entry 3475 (class 0 OID 18901)
-- Dependencies: 234
-- Data for Name: forgot_password_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.forgot_password_links (id, created_at, user_id) FROM stdin;
8aaa506f-ec56-4acb-a831-57876fa180b0	2023-07-29 14:08:28.680359+07	183
\.


--
-- TOC entry 3473 (class 0 OID 18848)
-- Dependencies: 232
-- Data for Name: loan_approvals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loan_approvals (id, loan_amount, loan_days_term, "receiverAccountNo", is_approved, user_id, created_at, rate, is_done) FROM stdin;
d082186c-098d-4ee7-bf3b-bb8e23aeca6a	30000	180	5859458120290690	t	266	2023-07-29 16:55:40.61318+07	5	t
6afa0850-2e84-42b5-acb3-5d26c6486564	30000	180	5859457287248296	t	125	2023-07-29 14:17:38.216169+07	5	\N
1d786af8-bd00-40ee-b21a-1c9a437158f6	300000	180	5859457287248296	t	125	2023-07-29 14:16:37.768023+07	5	\N
fa347016-85c9-4da3-aa0a-79b95f824f43	2000000	180	5859457287248296	f	125	2023-07-29 14:11:16.267905+07	5	\N
b87cf98a-9ecf-4f77-a668-1dbb5d2f21d1	40000	270	5859453815375927	t	349	2023-07-29 18:34:01.825682+07	6	t
55e0486f-6fc1-443f-a662-540208c3651d	50000	270	5859453815375927	t	349	2023-07-29 18:54:30.387277+07	6	t
220487e3-01e4-4c93-a310-25247dac1c07	100000	270	5859453815375927	t	349	2023-07-29 19:14:03.749709+07	6	t
1a94ec44-0209-4012-9a1d-28150ac3d097	100000	270	5859454508081710	t	366	2023-07-29 19:39:29.782014+07	6	t
6c9b3a5a-3206-4759-9180-201eeb843aa4	300000	180	5859453107378195	t	359	2023-07-29 19:05:42.382577+07	5	t
5e0e6210-2216-4805-8d02-f078e811ffc3	30000	180	5859459313519573	\N	368	2023-07-29 19:49:52.295496+07	5	\N
\.


--
-- TOC entry 3474 (class 0 OID 18855)
-- Dependencies: 233
-- Data for Name: loans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loans (id, is_payed, approval_id, created_at) FROM stdin;
dfd28fee-0435-43ad-bd01-3e8382e7997e	t	d082186c-098d-4ee7-bf3b-bb8e23aeca6a	2023-07-29 17:18:18.701437+07
6728aea9-300f-465d-b79d-7b7fa164a0ee	t	b87cf98a-9ecf-4f77-a668-1dbb5d2f21d1	2023-07-29 18:43:52.143033+07
f5e46eef-5be8-4ba0-b22b-326386d49966	t	55e0486f-6fc1-443f-a662-540208c3651d	2023-07-29 19:11:08.749551+07
0f50142d-2bbb-48cb-8a68-b9467df26272	t	220487e3-01e4-4c93-a310-25247dac1c07	2023-07-29 19:14:22.871009+07
645c76ad-af10-4787-92d0-88d7f99ac755	t	1a94ec44-0209-4012-9a1d-28150ac3d097	2023-07-29 19:40:01.497849+07
8ba6d046-44b7-4e11-92a0-828da31dfad7	t	6c9b3a5a-3206-4759-9180-201eeb843aa4	2023-07-29 19:12:38.814133+07
\.


--
-- TOC entry 3481 (class 0 OID 0)
-- Dependencies: 215
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 3482 (class 0 OID 0)
-- Dependencies: 217
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 3483 (class 0 OID 0)
-- Dependencies: 213
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- TOC entry 3484 (class 0 OID 0)
-- Dependencies: 221
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- TOC entry 3485 (class 0 OID 0)
-- Dependencies: 219
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);


--
-- TOC entry 3486 (class 0 OID 0)
-- Dependencies: 223
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 3487 (class 0 OID 0)
-- Dependencies: 225
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- TOC entry 3488 (class 0 OID 0)
-- Dependencies: 211
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- TOC entry 3489 (class 0 OID 0)
-- Dependencies: 209
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 30, true);


--
-- TOC entry 3490 (class 0 OID 0)
-- Dependencies: 228
-- Name: user_approvals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_approvals_id_seq', 18, true);


--
-- TOC entry 3491 (class 0 OID 0)
-- Dependencies: 230
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_uid_seq', 1, false);


-- Completed on 2023-07-29 19:52:56

--
-- PostgreSQL database dump complete
--

