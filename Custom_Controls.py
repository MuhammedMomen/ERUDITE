import flet as ft
import datetime




class CustomDataTable(ft.UserControl):
    
    def build(self):
        self.custom_data_table= ft.DataTable(
                width=700,
                bgcolor="bluegrey900",
                border=ft.border.all(3, "wdhite70"),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(3, "blue"),
                horizontal_lines=ft.border.BorderSide(1, "blue"),
                sort_column_index=0,
                sort_ascending=True,
                heading_row_color=ft.colors.BLACK12,
                heading_row_height=100,
                data_row_color={"hovered": "0x30FF0000"},
                show_checkbox_column=True,
                divider_thickness=0,
                column_spacing=200,
                columns=[
                    ft.DataColumn(
                        ft.Text("مبلغ"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                        numeric=True,
                    ),
                    ft.DataColumn(
                        ft.Text("النوع"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    ft.DataColumn(
                        ft.Text("النوع 3"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    
                ],
                rows=[
                    ft.DataRow(
                        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                        selected=True,
                        on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    ),
                    ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
                    ft.DataRow([ft.DataCell(ft.Text("C")), ft.DataCell(ft.Text("3"))]),
                ],
            )
        return ft.SafeArea(
            self.custom_data_table)
        



# New Class for DatePickerCard 
class DatePickerCard(ft.UserControl):
    
    def build(self):
        self.card_sahdow_color="system"
        self.card_fg_color="system"
        self.card_text_color="system"
        self.card_icon_color= "system"
        self.card_icon_size=20
        self.today_date= datetime.date.today()
        self.today_formatted_date = self.today_date.strftime("%d-%m-%y")
        
        self.date_field = ft.DatePicker(
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime(2100, 12, 31),
            current_date=datetime.datetime.now(),
            confirm_text="تأكيد",
            cancel_text="إلغاء",
            on_change=self.date_changed,
            help_text="التاريخ المختار هو",
            field_label_text="اختر تاريخ"

            
        )

        
        self.date_field_text = ft.Text(f"التاريخ  :{self.today_formatted_date}",color=self.card_text_color)
        self.date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH_ROUNDED,
            on_click=lambda _: self.date_field.pick_date(),
            icon_color= self.card_icon_color,
            icon_size=self.card_icon_size,
            
        
        )

        card_content = ft.Row(
            [self.date_button,self.date_field, self.date_field_text],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2
        )
        return ft.SafeArea(
            ft.Card(card_content, shadow_color=self.card_sahdow_color,color=self.card_fg_color),
            width=250,  # Optional width for better layout
        )

    def date_changed(self, e):
        self.date_field_text.value = f"التاريخ : {self.date_field.value.strftime('%d-%m-%y')}"
        self.update()  # Update the UserControl

# class FloatingMessages(ft.UserControl):
#     def build(self):
#         def change(e):
#             time.sleep(1)
#             self.stack.width=200
#             self.stack.height=200
#             self.stack.top=200
#             self.stack.bottom=200
#             self.stack.right=400
#             self.stack.left=300
#             self.stack.opacity=0.2
#             self.message.value="Hello There everybody"
#             time.sleep(1)
#             self.stack.width=50
#             self.stack.height=50
#             self.stack.top=200
#             self.stack.bottom=200
#             self.stack.right=400
#             self.stack.left=300
#             self.stack.opacity=0.0
#             self.message.value=""
#             self.update()

#         self.message=ft.Text("test here")
#         self.container=ft.Container(content=self.message,animate=ft.animation.Animation(1000, "bounceOut"),width=50, on_click=lambda e:change)
#         self.stack=ft.Stack([self.container])
#         return self.stack



class ThemeSwitch(ft.UserControl):
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page  # Store a reference to the Page object
        self.theme_mode = self.page.theme_mode  # Initialize with page's current theme
        self.icon= ft.icons.DARK_MODE_OUTLINED if self.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHTBULB_OUTLINE
        self.ThemeSwitchBtn = ft.IconButton(width=60, icon=self.icon, on_click=self.theme_changed)  # Set initial label based on current theme
        self.card_sahdow_color = "system"
        self.card_fg_color = "system"


    def theme_changed(self, e):
        self.theme_mode = ft.ThemeMode.DARK if self.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.icon= ft.icons.DARK_MODE_OUTLINED if self.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHTBULB_OUTLINE

        # Update the page's theme_mode property:
        self.page.theme_mode = self.theme_mode
        self.ThemeSwitchBtn.icon=self.icon
        

        # If necessary, trigger a page update:
        self.update()
        self.page.update()  # Potentially needed depending on ft.Page behavior

    def build(self) -> ft.Card:
        return ft.SafeArea(
            ft.Card(self.ThemeSwitchBtn, shadow_color=self.card_sahdow_color,color=self.card_fg_color),
              # Optional width for better layout
        )

class ExitConfirmation(ft.UserControl):
    def __init__(self, page: ft.Page,
                 confirmation_title="تأكيد الخروج", 
                 confirmation_message="هل أنت متأكد من الخروج من النظام؟",
                 on_confirm="نعم",
                 on_cancel="لا"):
        super().__init__()
        self.page = page
        self.page.window_prevent_close = True
        self.page.on_window_event = self.window_event
        self.confirmation_title = confirmation_title
        self.confirmation_message = confirmation_message
        self.on_confirm=on_confirm
        self.on_cancel=on_cancel

    def window_event(self, e):
        if e.data == "close":
            self.page.dialog = self.confirm_dialog
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self, e):
        self.page.window_destroy()


    def no_click(self, e):
        self.confirm_dialog.open = False
        self.page.update()

    def build(self):
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.confirmation_title),
            content=ft.Text(self.confirmation_message),
            actions=[
                ft.ElevatedButton(self.on_confirm, on_click=self.yes_click),
                ft.OutlinedButton(self.on_cancel, on_click=self.no_click),
            ],
            actions_alignment="end",
        )

        return ft.Container()


class Transaction_details(ft.UserControl):
    def build(self,
              trx_id= int,
              trx_amount= float,
              trx_category= enumerate,
              trx_SubCategory= enumerate,
              trx_SubCategory2= enumerate,
              trx_SubCategory3= enumerate,
              trx_acct= enumerate,
              trx_SubAcct2= enumerate,
              trx_SubAcct3= enumerate):
        
        self.trx_id=ft.TextField(value=trx_id)
        self.trx_amount=ft.TextField(value=trx_amount)
        self.trx_category=ft.TextField(value=trx_category)
        self.trx_SubCategory= ft.TextField(value=trx_SubCategory)
        self.trx_SubCategory2= ft.TextField(value=trx_SubCategory2)
        self.trx_SubCategory3= ft.TextField(value=trx_SubCategory3)
        self.trx_acct=ft.TextField(value=trx_SubCategory)
        self.trx_SubAcct2=ft.TextField(value=trx_SubAcct2)
        self.trx_SubAcct3=ft.TextField(value=trx_SubAcct3)
        

        return ft.SafeArea(ft.DataTable(columns=["#","مبلغ","نوع","تفصيل 1","تفصيلي 2"],rows=[self.trx_id,
                                                                                                self.trx_amount,
                                                                                                self.trx_category,
                                                                                                self.trx_SubCategory,
                                                                                                self.trx_SubCategory2,
                                                                                                self.trx_SubCategory3,
                                                                                                self.trx_acct,
                                                                                                self.trx_SubAcct2,
                                                                                                self.trx_SubAcct3]
                            ))
    
        
class register_page(ft.UserControl):
    pass

class login_page(ft.UserControl):
    pass

class Dashboard_page(ft.UserControl):
    pass

class Settings_page(ft.UserControl):
    pass


class Inputs_page(ft.UserControl):
    pass

class Transactions_page(ft.UserControl):
    pass

class Reports_page(ft.UserControl):
    pass


# # helper view
# def main(page: ft.Page):
#     page.rtl=True
#     page.theme_mode="Dark"

#     page.update()
#     page.add(DatePickerCard(),ThemeSwitch(page),CustomDataTable())
# ft.app(target=main)


