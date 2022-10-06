from typing import Dict, Optional, Tuple
from venv import create
from django.shortcuts import render, redirect
from django.views import View
from casino.models import User
from casino.helpers import (
    SYMBOL_DICT,
    re_roll_probability_by_30,
    re_roll_probability_by_60,
    generate_roll_values,
)


class Home(View):
    template_name: str = "home.html"

    def get(self, request):
        identity_key: Optional[str] = request.session.get("identity_key")
        if not identity_key:
            return redirect("casino:start")
        try:
            user = User.objects.get(identity_key=identity_key)
        except User.DoesNotExist:
            return redirect("casino:start")
        else:
            symbols = request.session.get("symbols") or ["N/A", "N/A", "N/A"]
            context: Dict = {
                "full_name": f"{user.first_name} {user.last_name}",
                "credit": user.credit,
                "symbols": symbols,
            }
        return render(request, self.template_name, locals())


class StartGame(View):
    """
    A class for start the game
    with entering user details
    """

    template_name: str = "start.html"

    def get(self, request):
        if identity_key := request.session.get("identity_key"):
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        email: Optional[str] = request.POST.get("email")
        first_name: Optional[str] = request.POST.get("first_name")
        last_name: Optional[str] = request.POST.get("last_name")

        user, created = User.objects.get_or_create(email=email)
        if user.is_active is False:
            user.is_active = True
            user.credit = 10
            user.save()
        if created:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        request.session["identity_key"] = user.identity_key
        return redirect("casino:home")


class RollView(View):
    template_name: str = "casino.html"

    def identify_win(self, choices: Tuple) -> Tuple:
        values: Tuple = generate_roll_values(3, choices)
        symbols: Tuple = self.__symbols(values)
        block_1, block_2, block_3 = values
        return block_1 == block_2 and block_1 == block_3, block_1, symbols

    def get(self, request):
        # User need to enter details if there is no record
        # exist for user in database
        identity_key: Optional[str] = request.session.get("identity_key")
        print("identity_key", identity_key)
        if not identity_key:
            return redirect("casino:start")

        # If user has 0 credits that's mean user cannot
        # play the game
        user = User.objects.get(identity_key=identity_key)
        user_credits: int = user.credit
        if user_credits == 0:
            return redirect("casino:stop")

        roll_values: Tuple = tuple(SYMBOL_DICT.keys())
        win, block, symbols = self.identify_win(roll_values)
        re_roll = 0
        if win:
            # Check re-roll probability
            if user_credits >= 40 and user_credits < 60:
                re_roll: int = re_roll_probability_by_30()
            elif user_credits >= 60:
                re_roll: int = re_roll_probability_by_60()

            # If re roll calculate new results
            if re_roll:
                win, block_number, symbols_names = self.identify_win(roll_values)
                if win:
                    block = block_number
                    symbols = symbols_names

            user.credit += SYMBOL_DICT.get(block, {}).get("reward")
        else:
            user.credit -= 1

        user.save()
        context: Dict = {
            "uuid": user.identity_key,
            "full_name": f"{user.first_name} {user.last_name}",
            "credit": user.credit,
            "symbols": symbols,
        }
        request.session["symbols"] = symbols
        return redirect("casino:home")
        # return render(request, self.template_name, locals())

    def __symbols(self, values: Tuple) -> Tuple:
        return tuple(
            SYMBOL_DICT.get(value, {}).get("name") for value in values
        )


class StopGameView(View):
    """
    A view is responsible for stop the game
    session for a user
    """

    def get(self, request):
        identity_key = request.session.get("identity_key")
        if not identity_key:
            redirect("/")
        user = User.objects.get(identity_key=identity_key)
        user.is_active = False
        user.credit = 0
        user.save()
        request.session.clear()
        return redirect("casino:start")
