
CREATE TABLE IF NOT EXISTS public.data_feed (
	ad_id text NULL,
	ad_insertion text NULL,
    "name" text NULL,
    image_url text NULL,
    main_category text NULL,
    category text NULL,
	description text NULL,
    price text NULL,
    region text NULL,
    url text NULL
    "condition" text NULL,
    ios_url text NULL,
    ios_app_store_id text NULL,
    ios_app_name text NULL,
    android_url text NULL,
    android_package text NULL,
    android_app_name text NULL,
	num_ad_replies text NULL,
);


COPY public.data_feed FROM '../src/utils/resources/feed1220.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed1240.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed2020.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed2060.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed3020.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed3040.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed3060.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed3080.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed4020.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed4080.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed5020.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed5040.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed5060.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed5160.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6020.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6060.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6080.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6100.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6120.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6140.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6160.csv' WITH FORMAT csv ;
COPY public.data_feed FROM '../src/utils/resources/feed6180.csv' WITH FORMAT csv ;

