import flet as ft

def main(page: ft.Page):
    page.title = "Flet Assignment App"
    page.padding = 20
    
    # store submitted data to display on Result page
    form_data = {
        "name": "",
        "dob": "",
        "gender": "",
        "address": "",
        "country": "",
    }
    
    # 1) LOGIN PAGE
    def show_login_page():
        page.clean()
        email_tf = ft.TextField(label="Email", width=260)
        pass_tf = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=260,
        )
        error_txt = ft.Text("", color="red", size=12)
        
        def handle_login(e):
            # show error if empty
            if email_tf.value.strip() == "" or pass_tf.value.strip() == "":
                error_txt.value = "Please enter email and password!"
                page.update()
                return
            # go to Home
            show_home_page()
            
        appbar = ft.AppBar(
            title=ft.Text("Flet Assignment App"),
            leading=None,
        )
        
        layout = ft.Column(
            [
                email_tf,
                pass_tf,
                ft.ElevatedButton("Log in", on_click=handle_login),
                error_txt,
            ],
            spacing=10,
        )
        page.add(appbar, layout)
        page.update()
    
    # 2) HOME PAGE
    def show_home_page():
        page.clean()
        
        def go_back_login(e):
            show_login_page()
            
        def go_form(e):
            show_form_page()
            
        back_btn = ft.ElevatedButton("Back", on_click=go_back_login)
        appbar = ft.AppBar(
            title=ft.Text("Home"),
            leading=back_btn,
        )
        
        layout = ft.Column(
            [
                ft.Text("Welcome!", size=20),
                ft.Text("Press the button below to open the form page.", size=14),
                ft.ElevatedButton("Go to Form", on_click=go_form),
            ],
            spacing=15,
        )
        page.add(appbar, layout)
        page.update()
    
    # 3) FORM PAGE
    def show_form_page():
        page.clean()
        
        def go_back_home(e):
            show_home_page()
            
        back_btn = ft.ElevatedButton("Back", on_click=go_back_home)
        appbar = ft.AppBar(
            title=ft.Text("Form"),
            leading=back_btn,
        )
        
        name_tf = ft.TextField(label="Name", width=300)
        
        # Date of Birth dropdowns
        dob_value = {"val": ""}
        day_options = [ft.dropdown.Option(str(d)) for d in range(1, 32)]
        month_options = [
            ft.dropdown.Option("01"),
            ft.dropdown.Option("02"),
            ft.dropdown.Option("03"),
            ft.dropdown.Option("04"),
            ft.dropdown.Option("05"),
            ft.dropdown.Option("06"),
            ft.dropdown.Option("07"),
            ft.dropdown.Option("08"),
            ft.dropdown.Option("09"),
            ft.dropdown.Option("10"),
            ft.dropdown.Option("11"),
            ft.dropdown.Option("12"),
        ]
        year_options = [ft.dropdown.Option(str(y)) for y in range(1960, 2026)]
        
        day_dd = ft.Dropdown(width=80, hint_text="Day", options=day_options)
        month_dd = ft.Dropdown(width=100, hint_text="Month", options=month_options)
        year_dd = ft.Dropdown(width=100, hint_text="Year", options=year_options)
        
        def update_dob(e):
            if (
                year_dd.value is not None
                and month_dd.value is not None
                and day_dd.value is not None
            ):
                d = day_dd.value.zfill(2)
                dob_value["val"] = f"{year_dd.value}-{month_dd.value}-{d}"
                page.update()
                
        day_dd.on_change = update_dob
        month_dd.on_change = update_dob
        year_dd.on_change = update_dob
        
        dob_section = ft.Column(
            [
                ft.Text("Date of Birth"),
                ft.Row([day_dd, month_dd, year_dd], spacing=10),
            ],
            spacing=5,
        )
        
        # Gender
        gender_rg = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value="Male", label="Male"),
                    ft.Radio(value="Female", label="Female"),
                    ft.Radio(value="Other", label="Other"),
                ],
                spacing=5,
            )
        )
        
        # Address
        address_tf = ft.TextField(
            label="Address",
            width=300,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        
        # Country
        country_dd = ft.Dropdown(
            label="Country",
            width=200,
            options=[
                ft.dropdown.Option("Finland"),
                ft.dropdown.Option("Sweden"),
                ft.dropdown.Option("Norway"),
                ft.dropdown.Option("Germany"),
            ],
        )
        
        error_msg = ft.Text("", color="red", size=12)
        
        def handle_submit(e):
            # all fields must be filled
            if (
                name_tf.value.strip() == ""
                or dob_value["val"] == ""
                or gender_rg.value is None
                or address_tf.value.strip() == ""
                or (country_dd.value is None or country_dd.value == "")
            ):
                error_msg.value = "Please fill all fields."
                page.update()
                return
            
            # save for result page
            form_data["name"] = name_tf.value.strip()
            form_data["dob"] = dob_value["val"]
            form_data["gender"] = gender_rg.value
            form_data["address"] = address_tf.value.strip()
            form_data["country"] = country_dd.value
            
            show_result_page()
            
        layout = ft.Column(
            [
                name_tf,
                dob_section,
                ft.Text("Gender"),
                gender_rg,
                address_tf,
                country_dd,
                ft.ElevatedButton("Submit", on_click=handle_submit),
                error_msg,
            ],
            spacing=15,
        )
        page.add(appbar, layout)
        page.update()
    
    # 4) RESULT PAGE
    def show_result_page():
        page.clean()
        
        def go_back_form(e):
            show_form_page()
            
        back_btn = ft.ElevatedButton("Back", on_click=go_back_form)
        appbar = ft.AppBar(
            title=ft.Text("Result"),
            leading=back_btn,
        )
        
        data = form_data.copy()
        details_card = ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("Result", size=18),
                        ft.Divider(),
                        ft.Row(
                            [
                                ft.Text("Name: " + data["name"]),
                                ft.Text("Date of Birth: " + data["dob"]),
                            ],
                            spacing=20,
                        ),
                        ft.Row(
                            [
                                ft.Text("Gender: " + data["gender"]),
                                ft.Text("Address: " + data["address"]),
                            ],
                            spacing=20,
                        ),
                        ft.Text("Country: " + data["country"]),
                        ft.Divider(),
                        ft.ElevatedButton("Go back", on_click=go_back_form),
                    ],
                    spacing=10,
                ),
            )
        )
        page.add(appbar, details_card)
        page.update()
    
    # start the app on login page
    show_login_page()

if __name__ == "__main__":
    ft.app(target=main)  # Fixed: Added missing closing parenthesis