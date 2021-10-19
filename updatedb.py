'''
Created on 6 Dec 2018
Updated 10 Feb 2021

@author: thomasgumbricht
'''

# Standard library imports

from os import path

# Third party imports

# Package application imports

#from geoimagine.gdalutilities import GDALstuff

class ProcessUpdateDB:
    '''class for layer updating'''   
    
    def __init__(self, pp, session):
        '''
        '''
        
        self.session = session
                
        self.pp = pp  
        
        self.verbose = self.pp.process.verbose   
        
        self.session._SetVerbosity(self.verbose)     
        
        # Direct to subprocess
 
        if self.verbose > 1:
            
            print ('    Starting ProcessLayout: ',self.pp.process.processid )
        
        
        if self.pp.process.processid == 'UpdateDbRegion':
            
            self._UpdateDbRegion()
            
        elif self.pp.process.processid == 'CreateLegend':
            
            self._AddRasterLegend()
            
        else:
            
            exitstr = 'Exiting, the updateDb process %s is not defined' %(self.pp.process.processid)
            
            exit(exitstr)
        
        
    def _UpdateDbRegion(self):
        '''
        '''
        
        # Loop over all locations, dates and compositions
        for locus in self.pp.dstLayerD:

            if len(self.pp.dstLayerD[locus]) == 0:
                
                exitstr = 'EXITING, no dates defined in updatedb._UpdateDbRegion'
                exit(exitstr)
            
            for datum in self.pp.dstLayerD[locus]:

                if len(self.pp.dstLayerD[locus][datum]) == 0:

                    exitstr = 'EXITING, no compositions defined in updatedb._UpdateDbRegion'
                    
                    print (exitstr)

                for comp in self.pp.dstLayerD[locus][datum]:
        
                    dstLayer = self.pp.dstLayerD[locus][datum][comp]
                    
                    if path.exists(dstLayer.FPN):
                        
                        if self.verbose == 2:
                            
                            infostr = '    Updating DB for region: %s, period: %s layer: %s with dataset file\n        %s'  %(locus, datum, comp, dstLayer.FPN)
                            
                            print (infostr)
 
                        if self.pp.dstLayerD[locus][datum][comp].comp.celltype != 'vector':

                            self.pp.dstLayerD[locus][datum][comp]._GetRastermetadata()
                                                    
                        if self.pp.process.delete:
                            
                            deleteDS = GDALstuff('',dstLayer.FPN,'')
                            
                            deleteDS.Delete()
                            
                            self.session._DeleteLayer(self.pp.dstLayerD[locus][datum][comp], self.pp.process.overwrite, self.pp.process.delete)


                        else:
                            
                            self.session._InsertLayer(self.pp.dstLayerD[locus][datum][comp], self.pp.process.overwrite, self.pp.process.delete)
                    
                    else: # # destination file does not exist
                        
                        if self.verbose > 1:
                            
                            infostr = '    No data source found for region: %s, period: %s layer: %s\n        (no file at: %s)'  %(locus, datum, comp, dstLayer.FPN)
                            
                            print (infostr)
                        
                        if self.pp.process.delete:
                            
                            if self.verbose == 2:
                                
                                print ('    Deleting layer from db anyway')
                                
                            self.session._DeleteLayer(self.pp.dstLayerD[locus][datum][comp], self.pp.process.overwrite, self.pp.process.delete)
                                
        if self.pp.process.delete:
            ''' NOT YET UPDATED
            '''
            #If all layers are removed, also delete the compostion
            for locus in self.process.dstLayerD:
                for datum in self.process.dstLayerD[locus]:
                    for dstcomp in self.process.dstLayerD[locus][datum]:
                        self.session._DeleteComposition(self.process.dstLayerD[locus][datum][dstcomp].comp)
                    return
