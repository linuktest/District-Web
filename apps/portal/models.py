from django.db import models


class SiteConfig(models.Model):
    """Admin-editable global site statistics and hero content."""
    total_clubs = models.IntegerField(default=0, help_text="Displayed on Impact Tracker")
    total_members = models.IntegerField(default=0, help_text="Displayed on Impact Tracker")
    volunteer_hours = models.IntegerField(default=0, help_text="Displayed on Impact Tracker")
    hero_tagline = models.CharField(max_length=255, default="Serve, Lead, Excel.")
    hero_subtext = models.TextField(blank=True)
    president_theme = models.TextField(blank=True, help_text="District President's theme statement")

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        """Enforce singleton — only one config record."""
        self.pk = 1
        super().save(*args, **kwargs)


class LeadershipProfile(models.Model):
    """District leadership — DEC, Directors, Zone Chairs."""
    ROLE_LEVELS = [
        ('DEC', 'District Executive Committee'),
        ('Director', 'Director'),
        ('Zone', 'Zone/Region Chairperson'),
    ]
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, help_text="e.g. District Governor")
    role_level = models.CharField(max_length=20, choices=ROLE_LEVELS)
    photo = models.ImageField(upload_to='leadership/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ['role_level', 'order', 'full_name']
        verbose_name = "Leadership Profile"

    def __str__(self):
        return f"{self.title} — {self.full_name}"


class Club(models.Model):
    """Leo Club registry."""
    CLUB_TYPE_CHOICES = [
        ('School', 'School-based'),
        ('Community', 'Community-based'),
    ]
    REGION_CHOICES = [('A', 'A'), ('B', 'B')]
    ZONE_CHOICES = [('A', 'A'), ('A1', 'A1'), ('B', 'B'), ('B1', 'B1')]
    name = models.CharField(max_length=150, unique=True)
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    zone = models.CharField(max_length=2, choices=ZONE_CHOICES)
    club_type = models.CharField(max_length=20, choices=CLUB_TYPE_CHOICES)
    president_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    facebook_url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='clubs/', blank=True, null=True)

    class Meta:
        ordering = ['region', 'zone', 'name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """District calendar events."""
    CATEGORY_CHOICES = [
        ('Council', 'Council Meeting'),
        ('District', 'District Project'),
        ('Club', 'Club Event'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    is_draft = models.BooleanField(default=True)
    president_attending = models.BooleanField(default=False, help_text="Check if the District President will be attending this event")

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"[{self.category}] {self.title}"

    @property
    def gcal_url(self):
        """Google Calendar 'Add to Calendar' link."""
        from urllib.parse import quote
        fmt = "%Y%m%dT%H%M%SZ"
        start = self.start_time.strftime(fmt)
        end = self.end_time.strftime(fmt)
        title = quote(self.title)
        details = quote(self.description[:200])
        loc = quote(self.location)
        return (
            f"https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text={title}&dates={start}/{end}&details={details}&location={loc}"
        )


class PressRelease(models.Model):
    """News & highlights shown on the Home page."""
    title = models.CharField(max_length=255)
    summary = models.TextField()
    published_at = models.DateField()
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='press/', blank=True, null=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
