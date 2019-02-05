import bcrypt
from django.db import models


class UserManager(models.Manager):
    @staticmethod
    def user_validator(post_data):
        errors = {}
        # Check for length
        if len(post_data["first_name"]) < 2:
            errors["first_name_len"] = "First name must have at least 2 characters"
        if len(post_data["last_name"]) < 2:
            errors["last_name_len"] = "Last name must have at least 2 characters"
        if len(post_data["email"]) < 2:
            errors["email_len"] = "Email must have at least 2 characters"
        if len(post_data["pw"]) < 8:
            errors["password_len"] = "Password must have at least 8 characters"
        # Make sure names are only letters
        if not post_data["first_name"].isalpha():
            errors["first_name_alpha"] = "First name must only contain letters"
        if not post_data["last_name"].isalpha():
            errors["last_name_alpha"] = "Last name must only contain letters"
        # Make sure email matches format
        # if not EMAIL_REGEX.match(post_data["email"]):
        #     errors["email_format"] = "Invalid email format"
        # Make sure email isn't already in the list
        if User.objects.filter(email=post_data["email"]):
            errors["email_used"] = "Email already in use"
        # Make sure both passwords match
        if post_data["pw"] != post_data["pw_confirm"]:
            errors["pw_match"] = "Passwords do not match"
        return errors

    @staticmethod
    def login_validator(post_data):
        errors = {}
        # Check if email is in the database
        if not User.objects.filter(email=post_data["email"]):
            errors["email_db_check"] = "Invalid credentials"
        # Check for correct password
        else:
            log_user = User.objects.filter(email=post_data["email"])[0]
            if not bcrypt.checkpw(post_data["pw"].encode(), log_user.pw_hash.encode()):
                errors["pw_db_check"] = "Invalid credentials"
        return errors

    # @staticmethod
    # def user_directory_path(instance, filename):
    #     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename> TODO: will it though?
    #     return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):  # Backpack, messenger, tote, travel, etc.
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Style(models.Model):  # BRB, Be Prepared, Be Charged, Be Spendy
    name = models.CharField(max_length=50, unique=True)
    categories = models.ManyToManyField(Category, related_name="styles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Collection(models.Model):  # Tokidoki, Sanrio, Blizzard, Classic, Legacy, Onyx, XY, Ever, Rose
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Print(models.Model):  # Each print is part of 1 collection - Sushi Cars, Hello Sanrio, Rainbow Dreams
    name = models.CharField(max_length=100, unique=True)
    collection = models.ForeignKey(
        Collection, related_name="prints", on_delete=models.CASCADE
    )
    styles = models.ManyToManyField(Style, related_name="prints")
    release_date = models.DateField(null=True, blank=True)
    # image = models.ImageField(
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bag(models.Model):  # Print: Super Toki, Style: Be Charged, Collection: Tokidoki, Category: Wallet
    print = models.ForeignKey(Print, related_name="bags", on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="bags")
    style = models.ForeignKey(Style, related_name="bags", on_delete=models.CASCADE)
    image = models.URLField(max_length=255, null=True, blank=True)
    image_resized = models.URLField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    pw_hash = models.CharField(max_length=255)
    about = models.TextField(max_length=1000, null=True, blank=True)
    # country =
    # avatar = models.ImageField()
    wants = models.ManyToManyField(Bag, related_name="wanted_by")
    haves = models.ManyToManyField(Bag, related_name="owned_by")
    # stash =
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
