#! /usr/bin/python
"""
    @Author_name : Arsham mohammadi nesyshabori
    @Author_email : arshammoh1998@gmail.com
    @Author_nickname : apep
    @date : 
    @version : 
"""

bot_token = "<your bot token>"
admin_password = "<set password for amdin>"
admin_telegram_id = None

successful_login_message = "شما با موفقیت وارد شدید"
fail_login_message = "اطلاعات وارد شده اشتباه است!"

successful_feed_back = "نظر شما با موفقیت ثبت شد"
successful_admin = "شما ادمین شدید"

wellcome_message = """\
به ربات اعلام نمرات دانشگاه خیام خوش آمدید.
این ربات برای سایت 
https://pooya.khayyam.ac.ir/
طراحی شده.
و در صورتی که استادی نمره ای را ثبت کند تغییر دهد یا تایید کند این ربات به شما اطلاع میدهد.
همچنین شما میتوانید برنامه امتحانی خود را مشاهده کنید.
نکته: درصورتی که پورتال شما به علت پرداخت نکردن هزینه دانشگاه بسته باشد این ربات نمیتواند فعالیت خود را به درستی انجام دهد.

برای شروع کار ربات 
یوزر و پسورد سایت خود را به صورت زیر وارد کنید 
توجه بین یوز و پسورد علامت : دونقطه وجود دارد و هیچ فاصله ای بین آن ها نیست
username:password
"""

info_message = """\
این ربات اوپن سورس است.
اطلاعات تماس با نویسنده ربات:
@Apep_1998
arshammoh1998@gmail.com
https://apep.ir
لینک گیت هاب ربات:
https://github.com/apep-1998/khayyamgradereport/
برای ارسال نظرات خود درباره ربات میتوانید پیامی به همین ربات که شامل  #نظر  باشد ارسال کنید.
"""

grade_text = """\
نمرات شما به شرح زیر میباشد.
"""

grade_change = "تغییر در {}\n"

exam_day = "زمان امتحانات شما به شرح زیر است."