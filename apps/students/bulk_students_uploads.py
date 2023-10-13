from apps.students.models import Student, StudentWallet
from apps.users.models import User

students = [{"first_name":"Annabal","last_name":"Gorvin","email":"agorvin3@guardian.co.uk","gender":"Female","id_number":"1146173360","phone_number":"+52 476 664 8897","reg_number":"UZ578967","status":"Active","student_type":"Boarder"},
{"first_name":"Bevvy","last_name":"Bartholomieu","email":"bbartholomieu4@senate.gov","gender":"Female","id_number":"7147345375","phone_number":"+7 392 614 4699","reg_number":"CY974258","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Davy","last_name":"Beechcraft","email":"dbeechcraft5@google.ca","gender":"Male","id_number":"0604800942","phone_number":"+63 281 884 8896","reg_number":"RL860565","status":"Active","student_type":"Boarder"},
{"first_name":"Barthel","last_name":"Tinline","email":"btinline6@tuttocitta.it","gender":"Male","id_number":"4927753857","phone_number":"+237 773 807 2522","reg_number":"FK842086","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Reginald","last_name":"Dollard","email":"rdollard7@tripod.com","gender":"Male","id_number":"4770526737","phone_number":"+86 998 436 5503","reg_number":"IZ022717","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Chase","last_name":"Guilder","email":"cguilder8@sourceforge.net","gender":"Male","id_number":"7892614207","phone_number":"+7 415 206 6428","reg_number":"GU700370","status":"Active","student_type":"Boarder"},
{"first_name":"Carver","last_name":"Duly","email":"cduly9@uol.com.br","gender":"Male","id_number":"2339955742","phone_number":"+62 255 741 3975","reg_number":"LS957254","status":"Active","student_type":"One-Time"},
{"first_name":"Bella","last_name":"Ferris","email":"bferrisa@etsy.com","gender":"Female","id_number":"8648025615","phone_number":"+7 240 967 9653","reg_number":"OL330407","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Galven","last_name":"Mayers","email":"gmayersb@dedecms.com","gender":"Male","id_number":"8050142422","phone_number":"+1 616 273 1742","reg_number":"IC102410","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Deny","last_name":"Alliston","email":"dallistonc@oakley.com","gender":"Female","id_number":"5942466666","phone_number":"+86 400 491 7003","reg_number":"MM125620","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Parrnell","last_name":"Rubenczyk","email":"prubenczykd@taobao.com","gender":"Male","id_number":"1462253311","phone_number":"+86 466 716 3506","reg_number":"HJ908314","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Barbe","last_name":"Wyllie","email":"bwylliee@ning.com","gender":"Female","id_number":"9188476260","phone_number":"+86 604 456 0411","reg_number":"HI647709","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Early","last_name":"Skottle","email":"eskottlef@e-recht24.de","gender":"Male","id_number":"3516062954","phone_number":"+63 667 573 5569","reg_number":"UE934956","status":"Active","student_type":"One-Time"},
{"first_name":"Barbey","last_name":"Heball","email":"bheballg@vk.com","gender":"Female","id_number":"9729541801","phone_number":"+86 470 108 2522","reg_number":"HR291203","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Yancey","last_name":"Filinkov","email":"yfilinkovh@list-manage.com","gender":"Male","id_number":"9320348464","phone_number":"+52 771 518 8712","reg_number":"QA196153","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Stacee","last_name":"Bullock","email":"sbullocki@nsw.gov.au","gender":"Male","id_number":"3778284860","phone_number":"+63 777 998 3965","reg_number":"DF636556","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Shelagh","last_name":"Scotchmur","email":"sscotchmurj@redcross.org","gender":"Female","id_number":"0928660083","phone_number":"+86 114 863 6408","reg_number":"RM713267","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Charlie","last_name":"Simoneau","email":"csimoneauk@oracle.com","gender":"Male","id_number":"6244764094","phone_number":"+1 282 922 2725","reg_number":"IO935335","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Jolyn","last_name":"Pammenter","email":"jpammenterl@miitbeian.gov.cn","gender":"Female","id_number":"3370610156","phone_number":"+48 616 310 3267","reg_number":"LF854706","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Coreen","last_name":"Mcimmie","email":"cmcimmiem@msu.edu","gender":"Female","id_number":"0710629458","phone_number":"+358 550 947 1267","reg_number":"YP925591","status":"Active","student_type":"Boarder"},
{"first_name":"Jenifer","last_name":"Mouget","email":"jmougetn@hp.com","gender":"Female","id_number":"8143309088","phone_number":"+62 629 410 3872","reg_number":"XB208227","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Abner","last_name":"Peris","email":"aperiso@businesswire.com","gender":"Male","id_number":"6522876318","phone_number":"+62 756 719 8121","reg_number":"WV465001","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Horatia","last_name":"Bullough","email":"hbulloughp@seesaa.net","gender":"Female","id_number":"4441362215","phone_number":"+355 357 195 4970","reg_number":"NM096632","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Gris","last_name":"Wimbury","email":"gwimburyq@narod.ru","gender":"Male","id_number":"7576859862","phone_number":"+880 368 787 6211","reg_number":"DW103640","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Cordie","last_name":"Pylkynyton","email":"cpylkynytonr@pen.io","gender":"Non-binary","id_number":"5341156233","phone_number":"+86 677 179 5868","reg_number":"WM659226","status":"Active","student_type":"One-Time"},
{"first_name":"Elsa","last_name":"De Beneditti","email":"edebenedittis@blinklist.com","gender":"Female","id_number":"3951201218","phone_number":"+54 364 728 6783","reg_number":"EG299243","status":"Active","student_type":"One-Time"},
{"first_name":"Lanie","last_name":"Marke","email":"lmarket@rambler.ru","gender":"Female","id_number":"1088595918","phone_number":"+62 466 676 2008","reg_number":"GW009953","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Danyelle","last_name":"Southworth","email":"dsouthworthu@tmall.com","gender":"Female","id_number":"9132901442","phone_number":"+299 389 982 7004","reg_number":"HB785363","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Kass","last_name":"Clarage","email":"kclaragev@engadget.com","gender":"Genderfluid","id_number":"9524345433","phone_number":"+62 831 648 6142","reg_number":"KL901407","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Deny","last_name":"Massot","email":"dmassotw@unicef.org","gender":"Female","id_number":"3031733688","phone_number":"+880 921 825 7850","reg_number":"JB133117","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Barny","last_name":"Routley","email":"broutleyx@discuz.net","gender":"Male","id_number":"3332652157","phone_number":"+86 497 787 9782","reg_number":"OA220780","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Ninette","last_name":"Seekings","email":"nseekingsy@amazon.co.jp","gender":"Female","id_number":"5561467754","phone_number":"+970 427 952 0453","reg_number":"DU489805","status":"Active","student_type":"Boarder"},
{"first_name":"Kane","last_name":"Treagus","email":"ktreagusz@youku.com","gender":"Male","id_number":"0845033002","phone_number":"+62 173 507 7261","reg_number":"QY207327","status":"Active","student_type":"One-Time"},
{"first_name":"Johann","last_name":"Janssens","email":"jjanssens10@fda.gov","gender":"Male","id_number":"9573405980","phone_number":"+48 685 643 8276","reg_number":"QL812945","status":"Active","student_type":"Boarder"},
{"first_name":"Solly","last_name":"Zuanelli","email":"szuanelli11@nsw.gov.au","gender":"Male","id_number":"2878843538","phone_number":"+7 348 996 6132","reg_number":"ED860639","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Sallyann","last_name":"Jillins","email":"sjillins12@meetup.com","gender":"Female","id_number":"1513498690","phone_number":"+976 568 641 2763","reg_number":"OR271329","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Vitia","last_name":"Swayton","email":"vswayton13@slideshare.net","gender":"Female","id_number":"2390654439","phone_number":"+86 789 668 0923","reg_number":"EV800544","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Denise","last_name":"Shepcutt","email":"dshepcutt14@timesonline.co.uk","gender":"Female","id_number":"6653096705","phone_number":"+56 832 538 8238","reg_number":"BD573499","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Tudor","last_name":"Dunsford","email":"tdunsford15@phoca.cz","gender":"Male","id_number":"8318866805","phone_number":"+55 721 491 5140","reg_number":"FZ592976","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Paton","last_name":"Killingbeck","email":"pkillingbeck16@skype.com","gender":"Male","id_number":"1831551814","phone_number":"+63 346 164 9246","reg_number":"VS307296","status":"Active","student_type":"One-Time"},
{"first_name":"Donnajean","last_name":"Bridgen","email":"dbridgen17@imageshack.us","gender":"Female","id_number":"7786302781","phone_number":"+380 285 409 5986","reg_number":"AP800205","status":"Active","student_type":"One-Time"},
{"first_name":"Jillie","last_name":"Mingus","email":"jmingus18@acquirethisname.com","gender":"Female","id_number":"3455982849","phone_number":"+46 338 425 8329","reg_number":"FT691104","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Gawain","last_name":"Driffe","email":"gdriffe19@taobao.com","gender":"Genderfluid","id_number":"7052110290","phone_number":"+358 430 261 3466","reg_number":"TS324407","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Reinaldos","last_name":"Filipczynski","email":"rfilipczynski1a@domainmarket.com","gender":"Male","id_number":"4376629069","phone_number":"+995 491 754 3120","reg_number":"QL898800","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Morton","last_name":"Kilduff","email":"mkilduff1b@cnet.com","gender":"Male","id_number":"7960410948","phone_number":"+48 131 433 1253","reg_number":"BL170695","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Katusha","last_name":"Bernath","email":"kbernath1c@ca.gov","gender":"Female","id_number":"9795386530","phone_number":"+93 588 349 2365","reg_number":"PT621506","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Merissa","last_name":"Roscoe","email":"mroscoe1d@cnn.com","gender":"Female","id_number":"4438920162","phone_number":"+374 962 749 5778","reg_number":"ZX033108","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Serge","last_name":"Dickons","email":"sdickons1e@php.net","gender":"Male","id_number":"9284189926","phone_number":"+86 879 967 1717","reg_number":"EI258195","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Margret","last_name":"Hamerton","email":"mhamerton1f@msu.edu","gender":"Female","id_number":"9287092782","phone_number":"+992 826 166 8718","reg_number":"RW791133","status":"Active","student_type":"Boarder"},
{"first_name":"Lorenzo","last_name":"Alred","email":"lalred1g@forbes.com","gender":"Male","id_number":"2426754140","phone_number":"+86 772 479 4189","reg_number":"YF410861","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Alessandro","last_name":"Yushin","email":"ayushin1h@comcast.net","gender":"Bigender","id_number":"5743762060","phone_number":"+353 185 220 0454","reg_number":"LY724237","status":"Active","student_type":"One-Time"},
{"first_name":"Felike","last_name":"Card","email":"fcard1i@aol.com","gender":"Male","id_number":"5588576993","phone_number":"+30 586 305 2742","reg_number":"WJ803055","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Smith","last_name":"Beckitt","email":"sbeckitt1j@yellowbook.com","gender":"Male","id_number":"4461043771","phone_number":"+62 310 673 0771","reg_number":"CH394501","status":"Active","student_type":"One-Time"},
{"first_name":"Kirsten","last_name":"Calterone","email":"kcalterone1k@oakley.com","gender":"Female","id_number":"2747090793","phone_number":"+86 418 741 2668","reg_number":"TC454482","status":"Active","student_type":"One-Time"},
{"first_name":"Blithe","last_name":"Chetwynd","email":"bchetwynd1l@washingtonpost.com","gender":"Female","id_number":"9739135001","phone_number":"+351 893 605 6162","reg_number":"FE675254","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Phylys","last_name":"Bedle","email":"pbedle1m@google.com.br","gender":"Female","id_number":"1992257647","phone_number":"+850 340 449 9800","reg_number":"GX055574","status":"Active","student_type":"One-Time"},
{"first_name":"Elnora","last_name":"Ryton","email":"eryton1n@cocolog-nifty.com","gender":"Female","id_number":"4441465452","phone_number":"+34 861 511 5424","reg_number":"GR025560","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Elnore","last_name":"Miklem","email":"emiklem1o@weebly.com","gender":"Agender","id_number":"6610496191","phone_number":"+62 598 384 3015","reg_number":"IQ383457","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Stefania","last_name":"Tennewell","email":"stennewell1p@hatena.ne.jp","gender":"Female","id_number":"2165867599","phone_number":"+86 542 495 7293","reg_number":"QR630633","status":"Active","student_type":"One-Time"},
{"first_name":"Justinn","last_name":"Wrefford","email":"jwrefford1q@plala.or.jp","gender":"Female","id_number":"8103347925","phone_number":"+1 612 985 9352","reg_number":"FN845552","status":"Active","student_type":"Boarder"},
{"first_name":"Elsy","last_name":"Haymes","email":"ehaymes1r@hud.gov","gender":"Female","id_number":"9687250576","phone_number":"+86 456 336 0699","reg_number":"AT519992","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Tommy","last_name":"Elcoat","email":"telcoat1s@state.gov","gender":"Agender","id_number":"8038144160","phone_number":"+86 290 265 2996","reg_number":"RP964720","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Cherey","last_name":"McClymond","email":"cmcclymond1t@constantcontact.com","gender":"Female","id_number":"5660900178","phone_number":"+86 507 616 7264","reg_number":"XO995553","status":"Active","student_type":"One-Time"},
{"first_name":"Gordon","last_name":"Maybery","email":"gmaybery1u@google.co.uk","gender":"Male","id_number":"7636531309","phone_number":"+591 830 727 9544","reg_number":"TD363698","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Bryan","last_name":"Lassen","email":"blassen1v@squarespace.com","gender":"Male","id_number":"4735110606","phone_number":"+62 650 423 4529","reg_number":"ZJ410202","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Stanislaus","last_name":"Hewson","email":"shewson1w@umn.edu","gender":"Male","id_number":"4600974312","phone_number":"+82 364 908 5094","reg_number":"OG636705","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Bernice","last_name":"Bradborne","email":"bbradborne1x@archive.org","gender":"Female","id_number":"2349914444","phone_number":"+47 875 757 5654","reg_number":"WE150837","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Alfreda","last_name":"Andersen","email":"aandersen1y@sina.com.cn","gender":"Female","id_number":"2199272763","phone_number":"+254 284 385 7420","reg_number":"ER156212","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Skyler","last_name":"Archibald","email":"sarchibald1z@google.com","gender":"Male","id_number":"7510869329","phone_number":"+86 860 728 0569","reg_number":"KJ069045","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Clea","last_name":"Deshorts","email":"cdeshorts20@google.nl","gender":"Female","id_number":"6063944745","phone_number":"+970 723 933 9523","reg_number":"YG500138","status":"Active","student_type":"Boarder"},
{"first_name":"Bartholomeus","last_name":"Sampey","email":"bsampey21@soup.io","gender":"Male","id_number":"1361906593","phone_number":"+33 644 748 8571","reg_number":"ZI959376","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Denys","last_name":"Hartshorn","email":"dhartshorn22@accuweather.com","gender":"Male","id_number":"9124341527","phone_number":"+62 809 176 5498","reg_number":"OC452200","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Hamid","last_name":"Gittoes","email":"hgittoes23@chron.com","gender":"Genderqueer","id_number":"8358534068","phone_number":"+57 646 348 1994","reg_number":"JR374764","status":"Active","student_type":"One-Time"},
{"first_name":"Jolee","last_name":"Gelsthorpe","email":"jgelsthorpe24@xinhuanet.com","gender":"Genderqueer","id_number":"7906443647","phone_number":"+86 247 725 3322","reg_number":"ET737721","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Hilton","last_name":"Persey","email":"hpersey25@yandex.ru","gender":"Male","id_number":"3304378126","phone_number":"+62 809 358 2067","reg_number":"SS475672","status":"Active","student_type":"Boarder"},
{"first_name":"Ramon","last_name":"Rumney","email":"rrumney26@symantec.com","gender":"Male","id_number":"9162456460","phone_number":"+7 689 611 7503","reg_number":"XO692555","status":"Active","student_type":"Boarder"},
{"first_name":"Angelina","last_name":"Luckham","email":"aluckham27@utexas.edu","gender":"Female","id_number":"2161547113","phone_number":"+53 331 684 5523","reg_number":"OF458850","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Melvyn","last_name":"Handaside","email":"mhandaside28@free.fr","gender":"Male","id_number":"0777483328","phone_number":"+62 317 837 8668","reg_number":"HW397836","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Imogene","last_name":"Shewery","email":"ishewery29@wix.com","gender":"Female","id_number":"4982336310","phone_number":"+63 226 617 1825","reg_number":"RN426222","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Haroun","last_name":"Mowlam","email":"hmowlam2a@nyu.edu","gender":"Male","id_number":"5766945137","phone_number":"+46 899 728 2562","reg_number":"YC359549","status":"Active","student_type":"One-Time"},
{"first_name":"Freddy","last_name":"Fischer","email":"ffischer2b@pinterest.com","gender":"Male","id_number":"5758550639","phone_number":"+86 328 973 9037","reg_number":"EZ262348","status":"Active","student_type":"One-Time"},
{"first_name":"Ebenezer","last_name":"Poker","email":"epoker2c@hibu.com","gender":"Male","id_number":"9207965726","phone_number":"+377 359 232 4114","reg_number":"DW894958","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Leanna","last_name":"Lages","email":"llages2d@answers.com","gender":"Female","id_number":"8793526460","phone_number":"+86 139 865 5106","reg_number":"SA489461","status":"Active","student_type":"One-Time"},
{"first_name":"Magdalene","last_name":"Crosland","email":"mcrosland2e@ovh.net","gender":"Female","id_number":"5127987564","phone_number":"+56 240 858 6815","reg_number":"WU868688","status":"Active","student_type":"Boarder"},
{"first_name":"Lesli","last_name":"Perryn","email":"lperryn2f@jalbum.net","gender":"Female","id_number":"6665490707","phone_number":"+44 492 898 7488","reg_number":"YW917236","status":"Active","student_type":"One-Time"},
{"first_name":"Clarice","last_name":"Priddie","email":"cpriddie2g@bloglines.com","gender":"Female","id_number":"2216960657","phone_number":"+86 229 769 3326","reg_number":"IV650622","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Desdemona","last_name":"Huegett","email":"dhuegett2h@opensource.org","gender":"Female","id_number":"9095315796","phone_number":"+86 153 903 7154","reg_number":"KR042153","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Ephrem","last_name":"McAuslan","email":"emcauslan2i@seesaa.net","gender":"Male","id_number":"3565428809","phone_number":"+62 325 186 5169","reg_number":"EI449799","status":"Active","student_type":"Pre-Paid"},
{"first_name":"Bradford","last_name":"Veltman","email":"bveltman2j@bloglovin.com","gender":"Male","id_number":"4429047446","phone_number":"+46 659 107 6966","reg_number":"HQ206921","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Dyanna","last_name":"Cheevers","email":"dcheevers2k@si.edu","gender":"Female","id_number":"3482209824","phone_number":"+967 423 579 3165","reg_number":"GJ504449","status":"Deactivated","student_type":"Boarder"},
{"first_name":"Madeleine","last_name":"Dearlove","email":"mdearlove2l@businessinsider.com","gender":"Non-binary","id_number":"0523920106","phone_number":"+993 961 659 1531","reg_number":"LP066139","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Miner","last_name":"Spendley","email":"mspendley2m@smh.com.au","gender":"Male","id_number":"3163312708","phone_number":"+63 978 518 6953","reg_number":"UF914149","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Perceval","last_name":"Kirkland","email":"pkirkland2n@sakura.ne.jp","gender":"Male","id_number":"6936121097","phone_number":"+52 799 704 9988","reg_number":"YK756576","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Leanora","last_name":"Ovid","email":"lovid2o@ezinearticles.com","gender":"Female","id_number":"1834258127","phone_number":"+54 977 527 9858","reg_number":"FK323735","status":"Deactivated","student_type":"Pre-Paid"},
{"first_name":"Paloma","last_name":"Mapes","email":"pmapes2p@webs.com","gender":"Female","id_number":"2129864750","phone_number":"+7 438 604 5036","reg_number":"FO196977","status":"Deactivated","student_type":"One-Time"},
{"first_name":"Ingar","last_name":"Rayburn","email":"irayburn2q@cyberchimps.com","gender":"Male","id_number":"3256692026","phone_number":"+55 739 486 1601","reg_number":"VF783894","status":"Active","student_type":"One-Time"},
{"first_name":"Orton","last_name":"Chesterfield","email":"ochesterfield2r@ameblo.jp","gender":"Male","id_number":"5068247589","phone_number":"+46 119 881 0242","reg_number":"IE823717","status":"Deactivated","student_type":"One-Time"}]


class BulkStudentsUploadMixin(object):
    def __init__(self):
        self.data = students


    def run(self):
        self.__upload_students()

    def __upload_students(self):
        students = self.data

        for student in students:
            username = student.get("id_number")
            email = student.get("email")
            first_name = student.get("first_name")
            last_name = student.get("last_name")
            gender = student.get("gender")
            phone_number = student.get("phone_number")
            id_number = student.get("id_number")
            registration_number = student.get("reg_number")
            student_type = student.get("student_type")
            status = student.get("status")

            user = User.objects.create(
                first_name=first_name, 
                last_name=last_name, 
                username=username,
                email=email,
                role="student",
                gender=gender,
                phone_number=phone_number,
                id_number=id_number
            )
            user.set_password("1234")
            user.save()

            student = Student.objects.create(
                registration_number=registration_number,
                user=user,
                student_type=student_type,
                status=status
            )

            wallet = StudentWallet.objects.create(
                student=student,
                balance=350 if student_type == "Boarder" else 0,
                total_spend_today=0
            )

            print("Student Successfully Uploaded!!")