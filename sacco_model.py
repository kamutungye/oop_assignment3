# OOP WITH PYTHON ASSIGNMENT 3

# *** QUESTION 2 ***
print("\n\n*** QUESTION 2 ***\n\n")

from abc import ABC, abstractmethod
import requests

class Member(ABC):
    def __init__(self, name, id_no, savings_balance):
        if not name or not isinstance(name, str):
            raise ValueError("Invalid name")
        if not id_no or not isinstance(id_no, str):
            raise ValueError("Invalid ID number")
        if not isinstance(savings_balance, (int, float)) or savings_balance < 0:
            raise ValueError("Savings balance must be a non-negative number")

        self.name = name
        self.id_no = id_no
        self.savings_balance = savings_balance

    @abstractmethod
    def loan_eligibility(self):
        pass

    @staticmethod
    def get_exchange_rate():
       
      #  Fetches the current USD to UGX exchange rate.
      #  Returns:
      #      float: Exchange rate UGX per 1 USD.
      #  Raises:
      #      Exception: On request or data parsing failure.
        
        try:
            response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)#predefined rates
            #response = requests.get("https://www.bou.or.ug/bouwebsite/ExchangeRates/", timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data["rates"]["UGX"]
            return rate
        except requests.exceptions.RequestException as e:
            raise ConnectionError("Network error while retrieving exchange rate.") from e
        except (KeyError, ValueError) as e:
            raise ValueError("Error parsing exchange rate data.") from e

    def display_loan_eligibility(self):
        try:
            ugx_amount = self.loan_eligibility()
            rate = self.get_exchange_rate()
            usd_equivalent = ugx_amount / rate
            print(f"{self.__class__.__name__} {self.name} (ID: {self.id_no})")
            print(f"  UGX Loan Eligibility: UGX {ugx_amount:,.0f}")
            print(f"  USD Equivalent: ${usd_equivalent:,.2f} (at rate UGX {rate:,.2f}/USD)")
        except Exception as e:
            print(f"Error calculating loan eligibility for {self.name}: {e}")


class FarmerMember(Member):
    def loan_eligibility(self):
        return 6 * self.savings_balance


class TraderMember(Member):
    def loan_eligibility(self):
        return 4 * self.savings_balance


# *** Example Usage ***
if __name__ == "__main__":
    try:
        members = [
            FarmerMember("Kamutungye", "Farmer001", 500_000),
            TraderMember("Saul", "Trader001", 800_000),
            FarmerMember("Patience", "Farmer002", 0),  # Edge case with 0 savings
        ]

        for member in members:
            member.display_loan_eligibility()

    except Exception as e:
        print(f"Application error: {e}")
