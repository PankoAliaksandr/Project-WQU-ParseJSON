# Import libraries
import pandas as pd
import numpy as np

# Class implementation
class NutrientsModel:
    
    # Constructor
    def __init__(self,
             main_df = pd.DataFrame(),
             food_df = pd.DataFrame(),
             zinc_df = pd.DataFrame(),
        ):
        self.__main_df = main_df
        self.__food_df = food_df
        self.__zinc_df = zinc_df

   # Parse JSON file
    def ParseFile(self):
        
        # read JSON file
        df_cut = pd.read_json("D:\./nutrients.json", lines=True)
        # convert meta column to miltiple columns
        meta_df = df_cut.meta.apply(pd.Series)
        # convert name column to miltiple columns
        name_df = df_cut.name.apply(pd.Series)
        # concatenate new dataframes
        new_df = pd.concat([df_cut.group, df_cut.manufacturer, meta_df, name_df,
                            df_cut.nutrients], axis = 1)
        # parse nutrients list
        new2_df = pd.concat([pd.DataFrame(x) for x in new_df['nutrients']], keys = new_df['ndb_no']).reset_index(level = 1, drop = True).reset_index()
        # merge data frames
        final_df = pd.merge(new2_df, new_df, how = 'left', on = 'ndb_no')
        self.__main_df = final_df.drop('nutrients',1)
        
    
    # Find amino acids food
    def FindAminoAcidsFood(self):
        
        # Acids
        acids_list = list(['Alanine','Arginine','Asparagine','Aspartic acid','Cysteine','Glutamine',
                           'Glutamic acid','Glycine','Histidine','Isoleucine','Leucine','Lysine','Methionine',
                           'Phenylalanine','Proline','Serine','Threonine','Tryptophan','Tyrosine','Valine'])
            
        # dictionary for every acid
        asid_dictionary = dict([(key,[]) for key in acids_list])
        
        # Fill dictionary values
        for i in range(len(self.__main_df)):
            if(self.__main_df.name[[i]].values[0] in asid_dictionary.keys()):
                key = self.__main_df.name[[i]].values[0]
                food_name = self.__main_df.long[[i]].values[0]
                asid_dictionary[key].append(food_name)
                
                
        # Create data frame 
        df_acids = pd.DataFrame(columns = ['Amino Acid', 'Food'] )
        
        for key,value in asid_dictionary.items():
            df_acids.loc[len(df_acids)] = [key,value]
        
        # Create acid food dataframe     
        self.__food_df = pd.concat([pd.DataFrame(x) for x in df_acids['Food']], keys = df_acids['Amino Acid']).reset_index(level = 1, drop = True).reset_index()   
        self.__food_df.columns = ['Amino Acid', 'Food']
        
        
    # Find Zinc median values
    def FindZincMedianValues(self):
        
        # Find unique group names
        groups_list = self.__main_df.group.unique()
        # Create a dictionary
        group_dictionary  = dict([(key,[]) for key in groups_list])
        
        for i in range(len(self.__main_df)):
            if(self.__main_df.abbr[[i]].values == 'ZN'):
                gr_name = self.__main_df.group[[i]].values[0]
                zn_value = self.__main_df.value[[i]].values[0]
                group_dictionary[gr_name].append(zn_value)
                
        
        # Calculate median
        self.__zinc_df = pd.DataFrame(columns = ['group_name', 'zn_mean_value'] )
        
        for key,value in group_dictionary.items():
            median = np.median([float(x) for x in group_dictionary[key]])
            self.__zinc_df.loc[len(self.__zinc_df)] = [key,median]
   
    
    # Show results
    def ShowResults(self):
        
        # Print amino acids group table
        print self.__food_df
        
        # Plot bar graph
        ax = self.__zinc_df.plot(x = 'group_name', y = 'zn_mean_value', kind = 'bar', legend = False)
        ax.set_xlabel('Group Name')
        ax.set_ylabel('Zn median value')
                
     # Main function
    def Main(self):
        
        # Parse JSON file
        self.ParseFile()
        # Find amino acids food
        self.FindAminoAcidsFood()
        # Find Zinc median values
        self.FindZincMedianValues()
        # Show results
        self.ShowResults()
        
# Create the instance of a class
nutrients_model = NutrientsModel()
                                         
# Call Main function of a class
nutrients_model.Main()
        

         
