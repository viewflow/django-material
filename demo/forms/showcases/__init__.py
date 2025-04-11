import django
from django.forms import Form as BaseForm

COUNTRY_CHOICES = (
    ("", "Country"),
    (1, "Afghanistan"),
    (2, "Albania"),
    (3, "Algeria"),
    (5, "Andorra"),
    (10, "Argentina"),
    (11, "Armenia"),
    (13, "Australia"),
    (14, "Austria"),
    (15, "Azerbaijan"),
    (16, "Bahamas"),
)

QUESTION_CHOICES = (
    ("X01", "I have a history of problems with anesthesia"),
    ("X02", "I smoke"),
    ("X03", "I have been addicted to recreational drugs"),
    ("X04", "I weak  eye contact lenses or glasses"),
    ("X05", "I have an implantable devise"),
    ("X06", "Blood has been donated for this procedure by a family member"),
    ("X07", "I consume alcohol on a regular basis"),
    (
        "X08",
        "I have teeth and mouth considerations such as loose teeth, caps, bridework, banding, and dentures",
    ),
    ("X09", "I have a vascular access devise"),
)

CARDIOVASCULAR_RISK_CHOICES = (
    ("R01", "Heart Attack"),
    ("R02", "Angina"),
    ("R03", "Congestive Heart Failure"),
    ("R04", "Previous heart surgery"),
    ("R05", "Heart Murmur"),
    ("R06", "Mitral Valve Prolapse"),
    ("R07", "Internal Defibrillator"),
    ("R08", "Paralysis"),
    ("R09", "Kidney Disease"),
    ("R10", "High Blood Pressure"),
    ("R11", "Fast or irregular heat beats"),
    ("R12", "Previous Angiosplasy"),
    ("R13", "Valvular Heart Disorder"),
    ("R14", "Aortic Stenosis"),
    ("R15", "Pacemaker"),
    ("R16", "Stroke"),
    ("R17", "Insulin Dependent Diabetes"),
    ("R18", "Shortness of Breath"),
)

APNIA_RISK_CHOICES = (
    ("A01", "Loud Snoring"),
    ("A02", "Choking while asleep"),
    ("A03", "Emphysema"),
    ("A04", "Pheumonia"),
    ("A05", "Bleeding Disorder"),
    ("A06", "Aids or HIV"),
    ("A07", "Jaundice"),
    ("A08", "Seizure Disorder"),
    ("A09", "Thyroid Trouble"),
    ("A10", "Joint Replacement"),
    ("A11", "Prostate problems"),
    ("A12", "Downs Syndrome"),
    ("A13", "Excessive Daytime Sleepiness"),
    ("A14", "Diagnsed Sleep Apnea"),
    ("A15", "Asthma"),
    ("A16", "TB"),
    ("A17", "Bruise Easy"),
    ("A18", "Hepatits"),
    ("A19", "Hiatal Hernia"),
    ("A20", "Migraine Headaches"),
    ("A21", "TMJ (temporomand joint problem)"),
    ("A22", "Kidney Problems"),
    ("A23", "Steroid Use"),
    ("A24", "Witnessed Grasping"),
    ("A25", "Bronchitis"),
    ("A26", "Wheezing"),
    ("A27", "Cystic Fibrosis"),
    ("A28", "Anemia"),
    ("A29", "Liver Desease"),
    ("A30", "Reflus"),
    ("A31", "Cancer"),
    ("A32", "Athritis"),
    ("A33", "Bladder Problems"),
    ("A34", "Cortisone Use"),
)


class SourceCodeMixin(object):
    def source(self):
        import inspect
        import itertools

        lines = inspect.getsourcelines(self.__class__)[0]
        lines = [
            x
            for x in itertools.takewhile(
                lambda x: not x.strip().startswith("template"), lines
            )
        ]
        return "".join(lines)


class Form(SourceCodeMixin, BaseForm):
    pass
