from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from tkinter import filedialog
#import ttp

class NPIWindow:   

    def clear_all(self):
        # clear things.  not sure yet.
        print('bleh?')

    def LoadFile(self):
        self.outdir.set('')
        self.filename.set('')
        #self.outfile.set('')
        try:
            self.t3browsebtn3.destroy()
            self.t3fintbx2.destroy()
            self.t3fnlabel2.destroy()
        except:
            pass

        # Input file     
        self.t3browsebtn = Button(self.tab3, text="Choose Input File", command=self.npiopen)        
        self.t3browsebtn.place(x=25, y=65)
        self.t3fintbx = Entry(self.tab3, state='readonly', textvariable=self.filename)
        self.t3fintbx.place(x=25, y=105, height=27, width=700)            

        # Output file     
        self.t3browsebtn2 = Button(self.tab3, text="Choose Output Directory", command=self.outputopen)
        self.t3browsebtn2.place(x=25, y=165)        
        self.t3fouttbx = Entry(self.tab3, state='readonly', textvariable=self.outdir)
        self.t3fouttbx.place(x=25, y=205, height=27, width=700)
        self.t3fnlabel1 = Label(self.tab3, textvariable=self.outfile)
        self.t3fnlabel1.place(x=200, y=168)

    def CopyPaste(self):
        
        self.t3browsebtn.destroy()
        self.t3fintbx.destroy()     
        self.t3browsebtn2.destroy()
        self.t3fouttbx.destroy()
        self.outdir.set('')
        self.filename.set('')
        self.t3fnlabel1.destroy()
        #self.outdir.set('')

        # Output file
        self.t3browsebtn3 = Button(self.tab3, text="Choose Output Directory", command=self.outputopen)        
        self.t3browsebtn3.place(x=25, y=65)
        self.t3fintbx2 = Entry(self.tab3, state='readonly', textvariable=self.outdir)
        self.t3fintbx2.place(x=25, y=105, height=27, width=700)
        self.t3fnlabel2 = Label(self.tab3, textvariable=self.outfile)
        self.t3fnlabel2.place(x=200, y=68)

    def npiopen(self):        
        filename = filedialog.askopenfilename()
        self.filename.set(filename)
    
    def outputopen(self):        
        outdir = filedialog.askdirectory()
        self.outdir.set(outdir)

    def __init__(self, win):

        #todo:   add menu - help option 
        
        # Use these lines to set window size based on current resolution
        #width  = win.winfo_screenwidth()
        #height = win.winfo_screenheight()
        #win.geometry('%sx%s' % (int(width/3), int(height/2)))
        win.geometry('900x600+250+200')
        states=("AL (ALABAMA)", "AK (ALASKA)", "AS (AMERICAN SAMOA)", "AZ (ARIZONA)", "AR (ARKANSAS)", "AA (ARMED FORCES AMERICAS)", "AE (ARMED FORCES EUROPE / CANADA / MIDDLE EAST / AFRICA)", "AP (ARMED FORCES PACIFIC)", "CA (CALIFORNIA)", "CO (COLORADO)", "CT (CONNECTICUT)", "DE (DELAWARE)", "DC (DISTRICT OF COLUMBIA)", "FM (FEDERATED STATES OF MICRONESIA)", "FL (FLORIDA)", "GA (GEORGIA)", "GU (GUAM)", "HI (HAWAII)", "ID (IDAHO)", "IL (ILLINOIS)", "IN (INDIANA)", "IA (IOWA)", "KS (KANSAS)", "KY (KENTUCKY)", "LA (LOUISIANA)", "ME (MAINE)", "MP (MARIANA ISLANDS, NORTHERN)", "MH (MARSHALL ISLANDS)", "MD (MARYLAND)", "MA (MASSACHUSETTS)", "MI (MICHIGAN)", "MN (MINNESOTA)", "MS (MISSISSIPPI)", "MO (MISSOURI)", "MT (MONTANA)", "NE (NEBRASKA)", "NV (NEVADA)", "NH (NEW HAMPSHIRE)", "NJ (NEW JERSEY)", "NM (NEW MEXICO)", "NY (NEW YORK)", "NC (NORTH CAROLINA)", "ND (NORTH DAKOTA)", "OH (OHIO)", "OK (OKLAHOMA)", "OR (OREGON)", "PA (PENNSYLVANIA)", "PR (PUERTO RICO)", "RI (RHODE ISLAND)", "SC (SOUTH CAROLINA)", "SD (SOUTH DAKOTA)", "TN (TENNESSEE)", "TX (TEXAS)", "UT (UTAH)", "VT (VERMONT)", "VI (VIRGIN ISLANDS)", "VA (VIRGINIA)", "WA (WASHINGTON)", "WV (WEST VIRGINIA)", "WI (WISCONSIN)", "WY (WYOMING)")
        countries=("AF (Afghanistan)", "AL (Albania)", "DZ (Algeria)", "AD (Andorra)", "AO (Angola)", "AI (Anguilla)", "AQ (Antarctica)", "AG (Antigua and Barbuda)", "AR (Argentina)", "AM (Armenia)", "AW (Aruba)", "AU (Australia)", "AT (Austria)", "AZ (Azerbaijan)", "BS (Bahamas)", "BH (Bahrain)", "BD (Bangladesh)", "BB (Barbados)", "BY (Belarus)", "BE (Belgium)", "BZ (Belize)", "BJ (Benin)", "BM (Bermuda)", "BT (Bhutan)", "BO (Bolivia)", "BA (Bosnia and Herzegovina)", "BW (Botswana)", "BV (Bouvet Island)", "BR (Brazil)", "IO (British Indian Ocean Territory)", "BN (Brunei Darussalam)", "BG (Bulgaria)", "BF (Burkina Faso)", "BI (Burundi)", "KH (Cambodia)", "CM (Cameroon)", "CA (Canada)", "CV (Cape Verde)", "KY (Cayman Islands)", "CF (Central African Republic)", "TD (Chad)", "CL (Chile)", "CN (China)", "CX (Christmas Island)", "CC (Cocos (Keeling Islands))", "CO (Colombia)", "KM (Comoros)", "CD (Congo, The Democratic Republic Of)", "CK (Cook Islands)", "CR (Costa Rica)", "HR (Croatia (Hrvatska))", "CI (Ctte D'Ivoire )", "CU (Cuba)", "CY (Cyprus)", "CZ (Czech Republic)", "DK (Denmark)", "DJ (Djibouti)", "DM (Dominica)", "DO (Dominican Republic)", "EC (Ecuador)", "EG (Egypt)", "SV (El Salvador)", "GQ (Equatorial Guinea)", "ER (Eritrea)", "EE (Estonia)", "ET (Ethiopia)", "FK (Falkland Islands (Malvinas))", "FO (Faroe Islands)", "FJ (Fiji)", "FI (Finland)", "FR (France)", "GF (French Guiana)", "PF (French Polynesia)", "TF (French Southern Territories)", "GA (Gabon)", "GM (Gambia)", "GE (Georgia)", "DE (Germany)", "GH (Ghana)", "GI (Gibraltar)", "GB (Great Britain (UK))", "GR (Greece)", "GL (Greenland)", "GD (Grenada)", "GP (Guadeloupe)", "GT (Guatemala)", "GG (Guernsey)", "GN (Guinea)", "GW (Guinea-Bissau)", "GY (Guyana)", "HT (Haiti)", "HM (Heard Island and McDonald Islands)", "VA (Holy See (Vatican City State))", "HN (Honduras)", "HK (Hong Kong)", "HU (Hungary)", "IS (Iceland)", "IN (India)", "ID (Indonesia)", "IR (Iran, Islamic Republic Of)", "IQ (Iraq)", "IE (Ireland)", "IM (Isle Of Man)", "IL (Israel)", "IT (Italy)", "JM (Jamaica)", "JP (Japan)", "JE (Jersey)", "JO (Jordan)", "KZ (Kazakhstan)", "KE (Kenya)", "KI (Kiribati)", "KP (Korea, D. Peoples Republic of)", "KR (Korea, Republic of)", "XK (Kosovo)", "KW (Kuwait)", "KG (Kyrgyzstan)", "LA (Lao Peoples Democratic Republic)", "LV (Latvia)", "LB (Lebanon)", "LS (Lesotho)", "LR (Liberia)", "LY (Libyan Arab Jamahiriya)", "LI (Liechtenstein)", "LT (Lithuania)", "LU (Luxembourg)", "MO (Macao)", "MK (Macedonia)", "MG (Madagascar)", "MW (Malawi)", "MY (Malaysia)", "MV (Maldives)", "ML (Mali)", "MT (Malta)", "MQ (Martinique)", "MR (Mauritania)", "MU (Mauritius)", "YT (Mayotte)", "MX (Mexico)", "MD (Moldova)", "MC (Monaco)", "MN (Mongolia)", "MS (Montserrat)", "MA (Morocco)", "MZ (Mozambique)", "MM (Myanmar)", "NA (Namibia)", "NR (Nauru)", "NP (Nepal)", "NL (Netherlands)", "AN (Netherlands Antilles)", "NC (New Caledonia)", "NZ (New Zealand)", "NI (Nicaragua)", "NE (Niger)", "NG (Nigeria)", "NU (Niue)", "NF (Norfolk Island)", "NO (Norway)", "OM (Oman)", "PK (Pakistan)", "PW (Palau)", "PS (Palestinian Territory, Occupied)", "PA (Panama)", "PG (Papua New Guinea)", "PY (Paraguay)", "PE (Peru)", "PH (Philippines)", "PN (Pitcairn)", "PL (Poland)", "PT (Portugal)", "QA (Qatar)", "RE (Reunion)", "RO (Romania)", "RU (Russian Federation)", "RW (Rwanda)", "KN (Saint Kitts and Nevis)", "SH (Saint Helena)", "LC (Saint Lucia)", "PM (Saint Pierre and Miquelon)", "VC (Saint Vincent and The Grenadines)", "WS (Samoa)", "SM (San Marino)", "ST (Sao Tome and Principe)", "SA (Saudi Arabia)", "SN (Senegal)", "CS (Serbia And Montenegro)", "SC (Seychelles)", "SL (Sierra Leone)", "SG (Singapore)", "SK (Slovakia)", "SI (Slovenia)", "SB (Solomon Islands)", "SO (Somalia)", "ZA (South Africa)", "GS (South Georgia and South Sandwich Isls)", "ES (Spain)", "LK (Sri Lanka)", "SD (Sudan)", "SR (Suriname)", "SJ (Svalbard and Jan Mayen Islands)", "SZ (Swaziland)", "SE (Sweden)", "CH (Switzerland)", "SY (Syrian Arab Republic)", "TW (Taiwan)", "TJ (Tajikistan)", "TZ (Tanzania, United Republic Of)", "TH (Thailand)", "TL (Timor-Leste)", "TG (Togo)", "TK (Tokelau)", "TO (Tonga)", "TT (Trinidad and Tobago)", "TN (Tunisia)", "TR (Turkey)", "TM (Turkmenistan)", "TC (Turks and Caicos Islands)", "TV (Tuvalu)", "UG (Uganda)", "UA (Ukraine)", "AE (United Arab Emirates)", "US (United States)", "UY (Uruguay)", "UM (US Minor Outlying Islands)", "UZ (Uzbekistan)", "VU (Vanuatu)", "VE (Venezuela)", "VN (Viet Nam)", "VG (Virgin Islands (British))", "WF (Wallis and Futuna Islands)", "EH (Western Sahara)", "YE (Yemen)", "ZM (Zambia)", "ZW (Zimbabwe)")
        self.filename = StringVar()
        self.outdir = StringVar()
        self.outfile = StringVar()
        self.outfile.set('Filename:   NPI20211214_0001.txt')

        self.t3browsebtn = Button()
        self.t3fintbx = Entry()        
        self.t3browsebtn2 = Button()
        self.t3fouttbx = Entry()

        # Initialize tabs
        self.tab_control = ttk.Notebook(win)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Lookup By NPI')
        self.tab_control.add(self.tab2, text='Lookup By Info')
        self.tab_control.add(self.tab3, text='Batch NPI Lookup')
        self.tab_control.add(self.tab4, text='Batch Info Lookup')
        self.tab_control.pack(expand=1, fill='both')

        self.LoadFile()

        # Lookup By NPI Tab 
        
        # NPI Text Box
        self.t1lbl1 = Label(self.tab1, text='NPI')
        self.t1lbl1.place(x=25, y=25)
        self.t1tbx1 = Entry(self.tab1, bd=2)
        self.t1tbx1.place(x=75, y=25)
        
        # Tab 1 Search button
        self.t1btn1 = Button(self.tab1, text='Search', bg="light blue")
        self.t1btn1.place(x=225, y=21, width=100)

        # First Name
        self.t1fnamelbl = Label(self.tab1, text='First Name: ')
        self.t1fnamelbl.place(x=25, y=75)
        self.t1fnameval = Label(self.tab1, text='sample')
        self.t1fnameval.place(x=125, y=75)

        # Last Name
        self.t1lnamelbl = Label(self.tab1, text='Last Name: ')
        self.t1lnamelbl.place(x=25, y=100)
        self.t1lnameval = Label(self.tab1, text='sample')
        self.t1lnameval.place(x=125, y=100)

        # Middle Name
        self.t1mnamelbl = Label(self.tab1, text='Middle Name: ')
        self.t1mnamelbl.place(x=25, y=125)
        self.t1mnameval = Label(self.tab1, text='sample')
        self.t1mnameval.place(x=125, y=125)

        # Taxonomy List
        self.t1taxlbl = Label(self.tab1, text='Taxonomy: ')
        self.t1taxlbl.place(x=25, y=150)
        self.t1taxval = Label(self.tab1, text='sample; can be multiple')
        self.t1taxval.place(x=125, y=150)

        # Addresses
        self.t1addrlbl = Label(self.tab1, text='Addresses: ')
        self.t1addrlbl.place(x=25, y=175)
        self.t1addrval = Label(self.tab1, text='sample; can be multiple')
        self.t1addrval.place(x=125, y=175)

        # Gender
        self.t1gendlbl = Label(self.tab1, text='Gender: ')
        self.t1gendlbl.place(x=25, y=200)
        self.t1gendval = Label(self.tab1, text='sample')
        self.t1gendval.place(x=125, y=200)

        # Status
        self.t1statlbl = Label(self.tab1, text='Status: ')
        self.t1statlbl.place(x=25, y=225)
        self.t1statval = Label(self.tab1, text='Active')
        self.t1statval.place(x=125, y=225)

        # Last Update Date
        self.t1updlbl = Label(self.tab1, text='Last Updated: ')
        self.t1updlbl.place(x=25, y=250)
        self.t1updval = Label(self.tab1, text='Eleventy Billion years ago')
        self.t1updval.place(x=125, y=250)

        # Credential
        self.t1credlbl = Label(self.tab1, text='Credential: ')
        self.t1credlbl.place(x=25, y=275)
        self.t1credval = Label(self.tab1, text='sample')
        self.t1credval.place(x=125, y=275)

        # Organization Name
        self.t1orglbl = Label(self.tab1, text='Organization: ')
        self.t1orglbl.place(x=25, y=300)
        self.t1orgval = Label(self.tab1, text='might not include this')
        self.t1orgval.place(x=125, y=300)

        # Other IDs
        self.t1idlbl = Label(self.tab1, text='Other IDs: ')
        self.t1idlbl.place(x=25, y=325)
        self.t1idval = Label(self.tab1, text='sample; can be multiple')
        self.t1idval.place(x=125, y=325)


        # Lookup By Info Tab 
        
        # NPI        
        # Todo:   use label for 1 npi returned, drop down box if multi
        self.t2npilbl = Label(self.tab2, text='NPI:')
        self.t2npilbl.place(x=25, y=25)
        self.t2npilbl2 = Label(self.tab2, text='<value(s) returned here upon clicking Search>')
        self.t2npilbl2.place(x=125, y=25)

        # First Name
        self.t2fnlbl = Label(self.tab2, text='First Name')
        self.t2fnlbl.place(x=25, y=75)
        self.t2fntbx = Entry(self.tab2, bd=2)
        self.t2fntbx.place(x=125, y=75)

        # Last Name
        self.t2lnlbl = Label(self.tab2, text='Last Name')
        self.t2lnlbl.place(x=25, y=100)
        self.t2lntbx = Entry(self.tab2, bd=2)
        self.t2lntbx.place(x=125, y=100)

        # Middle Name
        self.t2mnlbl = Label(self.tab2, text='Middle Name')
        self.t2mnlbl.place(x=25, y=125)
        self.t2mntbx = Entry(self.tab2, bd=2)
        self.t2mntbx.place(x=125, y=125)

        # Taxonomy Description
        # todo:  validate against Taxonomy.txt.   possibly provide a drop down?
        self.t2taxlbl = Label(self.tab2, text='Taxonomy Desc.')
        self.t2taxlbl.place(x=25, y=150)
        self.t2taxtbx = Entry(self.tab2, bd=2)
        self.t2taxtbx.place(x=125, y=150)

        # Address City       
        self.t2citylbl = Label(self.tab2, text='Address City')
        self.t2citylbl.place(x=25, y=175)
        self.t2citytbx = Entry(self.tab2, bd=2)
        self.t2citytbx.place(x=125, y=175)

        # Address State        
        self.t2statelbl = Label(self.tab2, text='Address State')
        self.t2statelbl.place(x=25, y=200)
        self.t2statecb = Combobox(self.tab2, values=states, width=17)
        self.t2statecb.place(x=125, y=200)

        # Address ZIP        
        self.t2ziplbl = Label(self.tab2, text='Address ZIP')
        self.t2ziplbl.place(x=25, y=225)
        self.t2ziptbx = Entry(self.tab2, bd=2)
        self.t2ziptbx.place(x=125, y=225)

        # Address Country Code         
        self.t2cntlbl = Label(self.tab2, text='Address Country')
        self.t2cntlbl.place(x=25, y=250)
        self.t2cntcb = Combobox(self.tab2, values=countries, width=17)
        self.t2cntcb.place(x=125, y=250)

        # Organization Name        
        self.t2orglbl = Label(self.tab2, text='Organization')
        self.t2orglbl.place(x=25, y=275)
        self.t2orgtbx = Entry(self.tab2, bd=2)
        self.t2orgtbx.place(x=125, y=275)

        # Tab 2 Search button
        self.t2btn1 = Button(self.tab2, text='Search', bg="light blue")
        self.t2btn1.place(x=90, y=325, width=110)

        # Batch NPI Lookup tab
        
        # Mode radio buttons
        self.t3frad1 = Radiobutton(self.tab3, text='Load from file', value=1, command=self.LoadFile)
        self.t3frad2 = Radiobutton(self.tab3, text='Copy/paste', value=2, command=self.CopyPaste)        
        self.t3frad1.place(x=10, y=10)
        self.t3frad2.place(x=125, y=10)
        self.t3frad1.select()
    