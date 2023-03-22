import hashlib
import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from application import dispatch
from dvadmin.utils.models import CoreModel, table_prefix

STATUS_CHOICES = (
    (0, "Enabled"),
    (1, "Disabled"),
)





class Users(CoreModel,AbstractUser):
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="User", help_text="User")
    email = models.EmailField(max_length=255, verbose_name="Email", null=True, blank=True, help_text="Email")
    mobile = models.CharField(max_length=255, verbose_name="Telephone", null=True, blank=True, help_text="Telephone")
    avatar = models.CharField(max_length=255, verbose_name="Avatar", null=True, blank=True, help_text="Avatar")
    name = models.CharField(max_length=40, verbose_name="Name", help_text="Name")
    GENDER_CHOICES = (
        (0, "Unknown"),
        (1, "Male"),
        (2, "Female"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="Gender", null=True, blank=True, help_text="Gender"
    )
    USER_TYPE = (
        (0, "Backed User"),
        (1, "Frontend User"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=0, verbose_name="User Type", null=True, blank=True, help_text="User Type"
    )
    post = models.ManyToManyField(to="Post",blank=True, verbose_name="Position", db_constraint=False, help_text="Position")
    role = models.ManyToManyField(to="Role", blank=True,verbose_name="Role", db_constraint=False, help_text="Role")
    dept = models.ForeignKey(
        to="Dept",
        verbose_name="Department",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="Department",
    )

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = "System Users"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Post(CoreModel):
    name = models.CharField(null=False, max_length=64, verbose_name="Position", help_text="Position")
    code = models.CharField(max_length=32, verbose_name="Position Code", help_text="Position Code")
    sort = models.IntegerField(default=1, verbose_name="Position Order", help_text="Position Order")
    STATUS_CHOICES = (
        (0, "Active"),
        (1, "Inactive"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Position Status", help_text="Position Status")

    class Meta:
        db_table = table_prefix + "system_post"
        verbose_name = "Positions"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="Role", help_text="Role")
    key = models.CharField(max_length=64, unique=True, verbose_name="Persmission Code", help_text="Permission Code")
    sort = models.IntegerField(default=1, verbose_name="Permission Order", help_text="Permission Order")
    status = models.BooleanField(default=True, verbose_name="Role Status", help_text="Role Status")
    admin = models.BooleanField(default=False, verbose_name="Isadmin", help_text="Isadmin")
    DATASCOPE_CHOICES = (
        (0, "Self Only Data Access"),
        (1, "Department and Subdepartment Data Access"),
        (2, "Department Data Access"),
        (3, "All Data Access"),
        (4, "Customized Data Access"),
    )
    data_range = models.IntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="Data Acess", help_text="Data Access")
    remark = models.TextField(verbose_name="Remark", help_text="Remark", null=True, blank=True)
    dept = models.ManyToManyField(to="Dept", verbose_name="Data Acsess-Department", db_constraint=False, help_text="Data Access-Department")
    menu = models.ManyToManyField(to="Menu", verbose_name="Menu", db_constraint=False, help_text="Menu")
    permission = models.ManyToManyField(
        to="MenuButton", verbose_name="Menu Button", db_constraint=False, help_text="Menu Button"
    )

    class Meta:
        db_table = table_prefix + "system_role"
        verbose_name = "Role"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Dept(CoreModel):
    name = models.CharField(max_length=64, verbose_name="Department", help_text="Department")
    key = models.CharField(max_length=64, unique=True,null=True,blank=True, verbose_name="Code", help_text="Code")
    sort = models.IntegerField(default=1, verbose_name="Order", help_text="Order")
    owner = models.CharField(max_length=32, verbose_name="Manager", null=True, blank=True, help_text="Manager")
    phone = models.CharField(max_length=32, verbose_name="Telephone", null=True, blank=True, help_text="Telphone")
    email = models.EmailField(max_length=32, verbose_name="Email", null=True, blank=True, help_text="Email")
    status = models.BooleanField(default=True, verbose_name="Department Status", null=True, blank=True, help_text="Department Status")
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Parent Department",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="Parent Department",
    )

    @classmethod
    def recursion_dept_info(cls, dept_id: int, dept_all_list=None, dept_list=None):
        """
        递归获取部门的所有下级部门
        :param dept_id: 需要获取的id
        :param dept_all_list: 所有列表
        :param dept_list: 递归list
        :return:
        """
        if not dept_all_list:
            dept_all_list = Dept.objects.values("id", "parent")
        if dept_list is None:
            dept_list = [dept_id]
        for ele in dept_all_list:
            if ele.get("parent") == dept_id:
                dept_list.append(ele.get("id"))
                cls.recursion_dept_info(ele.get("id"), dept_all_list, dept_list)
        return list(set(dept_list))

    class Meta:
        db_table = table_prefix + "system_dept"
        verbose_name = "Department"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Menu(CoreModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.CASCADE,
        verbose_name="Parent Menu",
        null=True,
        blank=True,
        db_constraint=False,
        help_text="Parent Menu",
    )
    icon = models.CharField(max_length=64, verbose_name="Menu Icon", null=True, blank=True, help_text="Menu Icon")
    name = models.CharField(max_length=64, verbose_name="Menu Name", help_text="Menu Name")
    sort = models.IntegerField(default=1, verbose_name="Order", null=True, blank=True, help_text="Order")
    ISLINK_CHOICES = (
        (0, "No"),
        (1, "Yes"),
    )
    is_link = models.BooleanField(default=False, verbose_name="Islink", help_text="Islink")
    is_catalog = models.BooleanField(default=False, verbose_name="Isdirectory", help_text="Isdirectory")
    web_path = models.CharField(max_length=128, verbose_name="Path", null=True, blank=True, help_text="Path")
    component = models.CharField(max_length=128, verbose_name="Component", null=True, blank=True, help_text="Component")
    component_name = models.CharField(max_length=50, verbose_name="Component Name", null=True, blank=True, help_text="Component Name")
    status = models.BooleanField(default=True, blank=True, verbose_name="Menu Status", help_text="Menu Status")
    cache = models.BooleanField(default=False, blank=True, verbose_name="Cache", help_text="Cache")
    visible = models.BooleanField(default=True, blank=True, verbose_name="Show on Side", help_text="Show on Side")

    class Meta:
        db_table = table_prefix + "system_menu"
        verbose_name = "Menu"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class MenuButton(CoreModel):
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="menuPermission",
        on_delete=models.CASCADE,
        verbose_name="Menu",
        help_text="Menu",
    )
    name = models.CharField(max_length=64, verbose_name="Name", help_text="Name")
    value = models.CharField(max_length=64, verbose_name="Permission", help_text="Permission")
    api = models.CharField(max_length=200, verbose_name="API", help_text="API")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="Request Method", null=True, blank=True, help_text="Request Method")

    class Meta:
        db_table = table_prefix + "system_menu_button"
        verbose_name = "Menu Button"
        verbose_name_plural = verbose_name
        ordering = ("-name",)


class Dictionary(CoreModel):
    TYPE_LIST = (
        (0, "text"),
        (1, "number"),
        (2, "date"),
        (3, "datetime"),
        (4, "time"),
        (5, "files"),
        (6, "boolean"),
        (7, "images"),
    )
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dictonary", help_text="Dictionary")
    value = models.CharField(max_length=200, blank=True, null=True, verbose_name="Code", help_text="Code")
    parent = models.ForeignKey(
        to="self",
        related_name="sublist",
        db_constraint=False,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Parent",
        help_text="Parent",
    )
    type = models.IntegerField(choices=TYPE_LIST, default=0, verbose_name="Data Type", help_text="Data Type")
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name="Color", help_text="Color")
    is_value = models.BooleanField(default=False, verbose_name="Isvalue", help_text="Isvalue, Store the Value")
    status = models.BooleanField(default=True, verbose_name="Status", help_text="Status")
    sort = models.IntegerField(default=1, verbose_name="Order", null=True, blank=True, help_text="Order")
    remark = models.CharField(max_length=2000, blank=True, null=True, verbose_name="Remark", help_text="Remark")

    class Meta:
        db_table = table_prefix + "system_dictionary"
        verbose_name = "Dictonary"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_dictionary()  # 有更新则刷新字典配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_dictionary()
        return res


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="Request Module", null=True, blank=True, help_text="Request Module")
    request_path = models.CharField(max_length=400, verbose_name="Request Path", null=True, blank=True, help_text="Request Path")
    request_body = models.TextField(verbose_name="Request Body", null=True, blank=True, help_text="Request Body")
    request_method = models.CharField(max_length=8, verbose_name="Request Method", null=True, blank=True, help_text="Request Method")
    request_msg = models.TextField(verbose_name="Request Msg", null=True, blank=True, help_text="Request Msg")
    request_ip = models.CharField(max_length=32, verbose_name="Request ID", null=True, blank=True, help_text="Requet IP")
    request_browser = models.CharField(max_length=64, verbose_name="Request Browser", null=True, blank=True, help_text="Request Browser")
    response_code = models.CharField(max_length=32, verbose_name="Response Code", null=True, blank=True, help_text="Response Code")
    request_os = models.CharField(max_length=64, verbose_name="Operating System", null=True, blank=True, help_text="Operating System")
    json_result = models.TextField(verbose_name="Json Reqult", null=True, blank=True, help_text="Json Result")
    status = models.BooleanField(default=False, verbose_name="Status", help_text="Status")

    class Meta:
        db_table = table_prefix + "system_operation_log"
        verbose_name = "System Log"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join("files", h[0:1], h[1:2], h + ext.lower())


class FileList(CoreModel):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="File", help_text="File")
    url = models.FileField(upload_to=media_file_name)
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="File md5", help_text="File md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + "system_file_list"
        verbose_name = "Files"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Area(CoreModel):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称")
    code = models.CharField(max_length=20, verbose_name="地区编码", help_text="地区编码", unique=True, db_index=True)
    level = models.BigIntegerField(verbose_name="地区层级(1省份 2城市 3区县 4乡级)", help_text="地区层级(1省份 2城市 3区县 4乡级)")
    pinyin = models.CharField(max_length=255, verbose_name="拼音", help_text="拼音")
    initials = models.CharField(max_length=20, verbose_name="首字母", help_text="首字母")
    enable = models.BooleanField(default=True, verbose_name="是否启用", help_text="是否启用")
    pcode = models.ForeignKey(
        to="self",
        verbose_name="父地区编码",
        to_field="code",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父地区编码",
    )

    class Meta:
        db_table = table_prefix + "system_area"
        verbose_name = "地区表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return f"{self.name}"


class ApiWhiteList(CoreModel):
    url = models.CharField(max_length=200, help_text="url", verbose_name="url")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="API Request Method", null=True, blank=True, help_text="API Request Method")
    enable_datasource = models.BooleanField(default=True, verbose_name="Enable Data Source", help_text="Enable Data Source", blank=True)

    class Meta:
        db_table = table_prefix + "api_white_list"
        verbose_name = "API White List"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class SystemConfig(CoreModel):
    parent = models.ForeignKey(
        to="self",
        verbose_name="Parent",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="Parent",
    )
    title = models.CharField(max_length=50, verbose_name="Title", help_text="Title")
    key = models.CharField(max_length=20, verbose_name="Key", help_text="Key", db_index=True)
    value = models.JSONField(max_length=100, verbose_name="Value", help_text="Value", null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name="Order", help_text="Order", blank=True)
    status = models.BooleanField(default=True, verbose_name="Status", help_text="Staus")
    data_options = models.JSONField(verbose_name="Data Options", help_text="Data Options", null=True, blank=True)
    FORM_ITEM_TYPE_LIST = (
        (0, "text"),
        (1, "datetime"),
        (2, "date"),
        (3, "textarea"),
        (4, "select"),
        (5, "checkbox"),
        (6, "radio"),
        (7, "img"),
        (8, "file"),
        (9, "switch"),
        (10, "number"),
        (11, "array"),
        (12, "imgs"),
        (13, "foreignkey"),
        (14, "manytomany"),
        (15, "time"),
    )
    form_item_type = models.IntegerField(
        choices=FORM_ITEM_TYPE_LIST, verbose_name="Form Type", help_text="Form Type", default=0, blank=True
    )
    rule = models.JSONField(null=True, blank=True, verbose_name="Rules", help_text="Rules")
    placeholder = models.CharField(max_length=50, null=True, blank=True, verbose_name="Placeholder", help_text="Placeholder")
    setting = models.JSONField(null=True, blank=True, verbose_name="Setting", help_text="Setting")

    class Meta:
        db_table = table_prefix + "system_config"
        verbose_name = "System Configuration"
        verbose_name_plural = verbose_name
        ordering = ("sort",)
        unique_together = (("key", "parent_id"),)

    def __str__(self):
        return f"{self.title}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_system_config()  # 有更新则刷新系统配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_system_config()
        return res


class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = ((1, "Normal"), (2, "QR Code"),)
    username = models.CharField(max_length=32, verbose_name="User", null=True, blank=True, help_text="User")
    ip = models.CharField(max_length=32, verbose_name="Login IP", null=True, blank=True, help_text="Login IP")
    agent = models.TextField(verbose_name="Agent", null=True, blank=True, help_text="Agent")
    browser = models.CharField(max_length=200, verbose_name="Browser", null=True, blank=True, help_text="Browser")
    os = models.CharField(max_length=200, verbose_name="OS", null=True, blank=True, help_text="OS")
    continent = models.CharField(max_length=50, verbose_name="州", null=True, blank=True, help_text="州")
    country = models.CharField(max_length=50, verbose_name="国家", null=True, blank=True, help_text="国家")
    province = models.CharField(max_length=50, verbose_name="省份", null=True, blank=True, help_text="省份")
    city = models.CharField(max_length=50, verbose_name="城市", null=True, blank=True, help_text="城市")
    district = models.CharField(max_length=50, verbose_name="县区", null=True, blank=True, help_text="县区")
    isp = models.CharField(max_length=50, verbose_name="运营商", null=True, blank=True, help_text="运营商")
    area_code = models.CharField(max_length=50, verbose_name="区域代码", null=True, blank=True, help_text="区域代码")
    country_english = models.CharField(max_length=50, verbose_name="Country", null=True, blank=True, help_text="Country")
    country_code = models.CharField(max_length=50, verbose_name="Country Code", null=True, blank=True, help_text="Country Code")
    longitude = models.CharField(max_length=50, verbose_name="Longitude", null=True, blank=True, help_text="Longitude")
    latitude = models.CharField(max_length=50, verbose_name="Altitude", null=True, blank=True, help_text="Altitude")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="Login Type", help_text="Login Type")

    class Meta:
        db_table = table_prefix + "system_login_log"
        verbose_name = "System Login Log"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenter(CoreModel):
    title = models.CharField(max_length=100,verbose_name="Title",help_text="Title")
    content = models.TextField(verbose_name="Content",help_text="Content")
    target_type=models.IntegerField(default=0,verbose_name="Target Type",help_text="Target Type")
    target_user = models.ManyToManyField(to=Users,related_name='user',through='MessageCenterTargetUser', through_fields=('messagecenter','users'),blank=True,verbose_name="目标用户",help_text="目标用户")
    target_dept = models.ManyToManyField(to=Dept,  blank=True, db_constraint=False,
                                    verbose_name="Target Department", help_text="Target Department")
    target_role = models.ManyToManyField(to=Role,  blank=True, db_constraint=False,
                                    verbose_name="Target Role", help_text="Target Role")

    class Meta:
        db_table = table_prefix + "message_center"
        verbose_name = "Message Center"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

class MessageCenterTargetUser(CoreModel):
    users = models.ForeignKey(Users,related_name="target_user", on_delete=models.CASCADE,db_constraint=False,verbose_name="Target User",help_text="Target User")
    messagecenter = models.ForeignKey(MessageCenter, on_delete=models.CASCADE,db_constraint=False,verbose_name="Message Center",help_text="Message Ceter")
    is_read = models.BooleanField(default=False,blank=True,null=True,verbose_name="Isread",help_text="Isread")

    class Meta:
        db_table = table_prefix + "message_center_target_user"
        verbose_name = "Message Center to User"
        verbose_name_plural = verbose_name
