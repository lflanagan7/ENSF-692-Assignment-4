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
        as long as the user input is within data_dogs. 

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
    # Create global variable to hold year_list so it can be accessed in main() to confirm years for data
    global year_list
    year_list = [str(i) for i in year_set]
    year_list.sort()
    year_list_output = " ".join(year_list)
    return year_list_output


def total_dogs(user_breed):
    """total_dogs: Finds the total number of dogs registered across all years for the given breed. 

        Args:
            user_breed(Breed): Breed object that has been updated based on user input. 

        Returns: total_dogs(int): An Integer representing total number of dogs registered. 
    """
    total_dogs = data_dogs[data_dogs['Breed'] == user_breed.breed]["Total"].sum()
    return total_dogs


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
    idx = pd.IndexSlice
    breed_all = pd.DataFrame(data_dogs[data_dogs["Breed"] == user_breed.breed])
    breed_year = breed_all.loc[idx[year,:]]["Total"].sum()
    all_dogs_year = data_dogs.loc[idx[year, :]]["Total"].sum()
    percent_year_output = format(breed_year / all_dogs_year, ".6%")
    return percent_year_output
    

def popular_months(user_breed):
    """popular_months: Finds the most popular months for registration of the given breed.

        Args:
        user_breed(Breed): Breed object that has been updated based on user input.

        Returns:
        pop_months_output(str): A String representing all of the most popular months. 
    """
    breed_all = pd.DataFrame(data_dogs[data_dogs["Breed"] == user_breed.breed])
    months = breed_all["Total"].groupby(level = "Month").count()
    max_value = months.max()
    months_freq = months.to_dict()
    popular_months = []
    for key, value in months_freq.items():
        if value == max_value:
            popular_months.append(key)
    popular_months_str = [str(i) for i in popular_months]
    pop_months_output = " ".join(popular_months_str)
    return pop_months_output

def main():

    # Import top dog breed data from excel file and create a Multi-Index DataFrame called data
    # Make data_dogs a global variable so that it can be accessed by functions defined above main()
    global data_dogs
    data_dogs = pd.read_excel(r"./CalgaryDogBreeds.xlsx", header = [0], index_col = [0, 1])
   
   # Create a new Breed object 
    user_breed = Breed()

    print("ENSF 692 Dogs of Calgary")
    # User input stage
    while True:
        try:
            user_input = input("Please enter a dog breed: ")

            # Update the Breed object based on the user input if the breed is listed within data_dogs.
            if user_input.upper() in data_dogs.values:
                user_breed.update_breed(user_input)

                # Data anaylsis stage
                # Call the approprate functions defined above to print the requested statistics for the given breed.
                print('The', user_breed.breed, 'was found in the top breeds for years: ', top_breed_years(user_breed))
                print('There have been', total_dogs(user_breed), user_breed.breed, 'dogs registered total.')

                # Print statistics if breed found in top breeds for 2021, or let user know that the breed was not in top breeds for 2021. 
                if "2021" in year_list:
                    print('The', user_breed.breed, 'was', percent_year(user_breed, 2021), 'of top breeds in 2021.')
                else:
                    print("The", user_breed.breed, "was not in the top breeds for 2021.")

                # Print statistics if breed found in top breeds for 2022, or let user know that the breed was not in top breeds for 2022.
                if "2022" in year_list:
                    print('The', user_breed.breed, 'was', percent_year(user_breed, 2022), 'of top breeds in 2022.')
                else:
                    print("The", user_breed.breed, "was not in the top breeds for 2022.")

                # Print statistics if breed found in top breeds for 2023, or let user know that the breed was not in top breeds for 2023.
                if "2023" in year_list:
                    print('The', user_breed.breed, 'was', percent_year(user_breed, 2023), 'of top breeds in 2023.')
                else: 
                    print("The", user_breed.breed, "was not in the top breeds for 2023.")

                # Call the approprate functions defined above to print the requested statistics for the given breed
                print('The', user_breed.breed, 'was', percent_all_years(user_breed), 'of top breeds across all years.')
                print('Most popular month(s) for', user_breed.breed, ':', popular_months(user_breed) )
                
                # End program after successful data analysis and entry. 
                break

            # If user does not enter a breed listed within data_dogs, display message to let them know input is invalid. 
            # Handle error so that program will continue asking for inputs until successful entry and data analysis. 
            else:
                raise KeyError("Dog breed not found in the data. Please try again.")
            
        except KeyError as err:
            print(err)


if __name__ == '__main__':
    main()
