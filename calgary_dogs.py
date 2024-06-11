# calgary_dogs.py
# Laurel Flanagan 

# A terminal-based application for computing and printing statistics based on given input.

import numpy as np 
import pandas as pd 


class Breed:
    """A class used to create a Breed object. 

        Attributes:
        breed (str): String that represents a dog breed within Calgary's top dog breeds for 2021, 
        2022 and/or 2023. Default String is updated based on user input. 
    """
    def __init__(self):
            self.breed = ''

    def update_breed(self, user_input):
      """update_breed: Update the dog breed associated with the Breed object based on the user input, 
        as long as the user input is within the data_dogs DataFrame. 

        Args:
            user_input(str): String entered by the user that represents a dog breed. 

        Returns:
            None  
      """
      if user_input.upper() in data_dogs.values:
        self.breed = user_input.upper()


def top_breed_years(user_breed): 
    """top_breed_years: Find the years for which the given breed is listed within data_dogs. 

        Args:
            user_breed(Breed): Breed object that has been updated based on user input.  

        Returns: 
            year_list_output(str): A String of all years the given breed is listed within data_dogs.
    """
    breed_all = pd.DataFrame(data_dogs[data_dogs["Breed"] == user_breed.breed])
    years = breed_all.index.get_level_values("Year")
    year_set = {str(n) for n in years}
    # Create global variable to hold year_list so it can be accessed in main() to confirm years available for other statistics
    global year_list
    year_list = [str(i) for i in year_set]
    year_list.sort()
    year_list_output = " ".join(year_list)
    return year_list_output


def total_dogs(user_breed):
    """total_dogs: Finds the total number of dogs registered across all years for the given breed. 

        Args:
            user_breed(Breed): Breed object that has been updated based on user input. 

        Returns: total_dogs_output(int): An Integer representing total number of dogs registered. 
    """
    total_dogs_output = data_dogs[data_dogs['Breed'] == user_breed.breed]["Total"].sum()
    return total_dogs_output


def percent_all_years(user_breed):
    """percent_all_years: Finds the percentage of registrations for the given breed out of the 
        total registrations for all top breeds in data_dogs. 
    
        Args:
        user_breed(Breed): Breed object that has been updated based on user input. 

        Returns: percent_all_years_output(str): A String representing the percentage of registrations 
        for the given breed out of total registrations. 
    """
    breed_all_years = data_dogs[data_dogs['Breed'] == user_breed.breed]["Total"].sum()
    all_dogs_years = data_dogs["Total"].sum()
    percent_all_years_output = format(breed_all_years / all_dogs_years, ".6%")
    return percent_all_years_output

def percent_year(user_breed, year):
    """percent_year: Finds the percentage of registrations for the given breed out of the 
        total registrations for all top breeds in data_dogs, for a given year. 

        Args:
        user_breed(Breed): Breed object that has been updated based on user input.
        year(int): Integer representing the given year. 

        Returns: percent_year_output(str): A String representing the percentage of registrations for 
        the given year for the given breed out of total registrations. 
    """
    breed_all = pd.DataFrame(data_dogs[data_dogs["Breed"] == user_breed.breed])
    idx = pd.IndexSlice
    breed_year = breed_all.loc[idx[year,:]]["Total"].sum()
    all_dogs_year = data_dogs.loc[idx[year, :]]["Total"].sum()
    percent_year_output = format(breed_year / all_dogs_year, ".6%")
    return percent_year_output
    

def popular_months_by_year(user_breed, year):
    """popular_months: Finds the most popular months for registration (highest total number of registrations) 
        of the given breed, in a given year (2021, 2022, or 2023).

        Args:
        user_breed(Breed): Breed object that has been updated based on user input.
        year(int): Integer representing the given year. 

        Returns:
        pop_months_output(str): A String representing the most popular months (months with highest 
        registration numbers) for the given breed for a specific year. 
    """
    breed_all = pd.DataFrame(data_dogs[data_dogs["Breed"] == user_breed.breed])
    idx = pd.IndexSlice
    months_totals = breed_all.loc[idx[year, :]]["Total"].groupby(level = "Month").sum()
    max_value = months_totals.max()
    months_dict = months_totals.to_dict()
    # Include any tied months by getting all keys from the dict for which the sum of total registrations value is equal to the max 
    pop_months = [str(key) for key, value in months_dict.items() if value == max_value]
    pop_months_output =" ".join(pop_months)
    return pop_months_output


def popular_months_overall(user_breed):
    """popular_months: Finds the most popular months for registration of the given breed overall 
        (including all years of registrations that the given breed was in the top dog breeds).

        Args:
        user_breed(Breed): Breed object that has been updated based on user input.

        Returns:
        pop_months_overall_output(str): A String representing the most popular months (months with
        highest total registration numbers including all years) for a given breed. 
    """
    breed_all = pd.DataFrame(data_dogs[data_dogs["Breed"] == user_breed.breed])
    months_totals_overall = breed_all["Total"].groupby(level = "Month").sum()
    max_value_overall = months_totals_overall.max()
    months_overall_dict = months_totals_overall.to_dict()
    # Include any tied months by getting all keys from the dict for which the sum of total registrations value is equal to the max 
    pop_months_overall = [str(key) for key, value in months_overall_dict.items() if value == max_value_overall]
    pop_months_overall_output = " ".join(pop_months_overall)

    return pop_months_overall_output 


def main():

    # Import top dog breed data from excel file and create a Multi-Index DataFrame called data_dogs (indices for year and month)
    # Make data_dogs a global variable so that it can be accessed by functions defined above main()
    global data_dogs
    data_dogs = pd.read_excel(r"./CalgaryDogBreeds.xlsx", header = [0], index_col = [0, 1])
   
   # Create a new Breed object 
    user_breed = Breed()

    print("ENSF 692 Dogs of Calgary")
    # User input stage
    while True:
        try:
            # Prompt for user input 
            user_input = input("Please enter a dog breed: ")

            # Update the Breed object based on the user input if the breed is listed within data_dogs.
            if user_input.upper() in data_dogs.values:
                user_breed.update_breed(user_input)

                # Data anaylsis stage
                # Call the approprate functions defined above to print the requested statistics for the given breed.
                print('The', user_breed.breed, 'was found in the top breeds for years: ', top_breed_years(user_breed))
                print('There have been', total_dogs(user_breed), user_breed.breed, 'dogs registered total.')

                # Print statistics if breed found in top breeds for 2021, or note that the breed was not in top breeds for 2021. 
                if "2021" in year_list:
                    print('The', user_breed.breed, 'was', percent_year(user_breed, 2021), 'of top breeds in 2021.')
                else:
                    print("The", user_breed.breed, "was not in the top breeds for 2021.")

                # Print statistics if breed found in top breeds for 2022, or note that the breed was not in top breeds for 2022.
                if "2022" in year_list:
                    print('The', user_breed.breed, 'was', percent_year(user_breed, 2022), 'of top breeds in 2022.')
                else:
                    print("The", user_breed.breed, "was not in the top breeds for 2022.")

                # Print statistics if breed found in top breeds for 2023, or note that the breed was not in top breeds for 2023.
                if "2023" in year_list:
                    print('The', user_breed.breed, 'was', percent_year(user_breed, 2023), 'of top breeds in 2023.')
                else: 
                    print("The", user_breed.breed, "was not in the top breeds for 2023.")

                # Call the approprate function defined above to print the requested statistics for the given breed.
                print('The', user_breed.breed, 'was', percent_all_years(user_breed), 'of top breeds across all years.')

                # Provide most popular month(s) overall (month(s) with highest total number of registrations across all years the breed was in top breed).
                print('Most popular month(s) for', user_breed.breed, 'dogs:')
                print("\t", "Overall (including all years", user_breed.breed, "was in top breeds):", popular_months_overall(user_breed))
                
                # Print most popular month(s)for breed in 2021 if breed found in top breeds for 2021, or note that breed was not in top breeds for 2021. 
                if "2021" in year_list: 
                    print("\t", "2021:", popular_months_by_year(user_breed, 2021))
                else: 
                    print("\t", "2021:", user_breed.breed, "was not in top breeds for 2021")
                    
                # Print most popular month(s) for breed in 2022 if breed found in top breeds for 2022, or note that breed was not in top breeds for 2022. 
                if "2022" in year_list: 
                    print("\t", "2022:", popular_months_by_year(user_breed, 2022))
                else: 
                    print("\t", "2022:", user_breed.breed, "was not in top breeds for 2022.")

                # Print most popular month(s) for breed in 2023 if breed found in top breeds for 2023, or note that breed was not in top breeds for 2023. 
                if "2023" in year_list: 
                    print("\t", "2023:", popular_months_by_year(user_breed, 2023))
                else: 
                    print("\t", "2023:", user_breed.breed, "was not in top breeds for 2023.")

                # End program after successful data analysis and entry. 
                break

            # If user does not enter a breed listed within data_dogs, display message to let them know input is invalid. 
            # Handle error so that program will continue asking for inputs until successful entry and data analysis. 
            else:
                raise KeyError("Dog breed not found in the data. Please try again.")
            
        except KeyError as err:
            e = err.args[0]
            print(e)


if __name__ == '__main__':
    main()
