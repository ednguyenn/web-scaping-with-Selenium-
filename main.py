from market.market import Market
import pandas as pd 

if __name__ == "__main__":
    bot = Market()  # Prevent the browser from quitting automatically
    #land the first page
    bot.land_first_page()
    #enter the desired postcode to scape data
    bot.enter_postcode()
    
    bot.select_first_postcode_option()
    bot.click_read_catalogue_button()
    
    categories, category_list = bot.get_category_list()
    example_category = categories[0]
    example_category.click()
    
    category_data = bot.extract_products_in_category()
    df = pd.DataFrame(category_data)
    print(df)
    
    
    #to do list
    #succeffully extract data from 1 category,
    #need extract data from all categories
    #need to join all dataframe together after extraction 
    #add categories column into dataframe
    #add supermarket name (optional)
    #clean data and save it to csv for further analysis