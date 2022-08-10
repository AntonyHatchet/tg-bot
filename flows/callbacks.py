from enum import Enum


class Callbacks(Enum):
    main_menu = 0
    about = 1
    consultation = 2
    consultation_litigation = 2.1
    consultation_business = 2.2
    consultation_property = 2.3
    consultation_copyright = 2.4
    consultation_inheritance = 2.5
    consultation_bankrupt = 2.6
    consultation_pension = 2.7
    consultation_other = 2.8
    consultation_type_personal = 2.9
    consultation_type_phone = 2.10
    consultation_type_letter = 2.11
    consultation_phone_price_other = 2.12
    consultation_phone_price_self = 2.13
    consultation_personal_price_other = 2.14
    consultation_personal_price_self = 2.15
    pro_bono = 3
    pro_bono_yes = 3.1
    angels = 4
    angels_yes = 4.1
    other = 5
    other_media = 5.1
    other_media_yes = 5.2
    other_media_no = 5.3
    other_subscribe = 5.4
    other_faq = 5.5
    other_faq_jurist = 5.6
    other_faq_lawyer = 5.7
    other_faq_entrepreneur = 5.8
    other_faq_regular = 5.9
    other_faq_servant = 5.10
    other_club = 5.11
    other_club_yes = 5.12
    other_jobs = 5.13
    other_cooperation = 5.14
    other_cooperation_media = 5.15
    other_cooperation_gov = 5.16
    other_cooperation_isntitute = 5.17
    other_cooperation_other = 5.18
