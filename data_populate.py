from rent_json import RentData
from util import s3_file_download,s3_move_file
import os
from datetime import datetime


def download_file():
    bucket=os.environ['S3_BUCKET']

    out_format='%Y%m%d'
    to_day=datetime.today().strftime(out_format)
    file_name="immobilienscout24_berlin_"+to_day+".json"
    s3_file_path = 'Alpha/pandas/{file_name}'.format(file_name=file_name)
    output_file='/data/CSV/'+file_name

    s3_file_download(bucket,s3_file_path,output_file)

    return s3_file_path,output_file




contactDetails = ['id', 'contactDetails_id', 'contactDetails_address_city', 'contactDetails_address_houseNumber',
                  'contactDetails_address_postcode', 'contactDetails_address_street', 'contactDetails_cellPhoneNumber',
                  'contactDetails_cellPhoneNumberAreaCode', 'contactDetails_cellPhoneNumberCountryCode',
                  'contactDetails_cellPhoneNumberSubscriber', 'contactDetails_company', 'contactDetails_countryCode',
                  'contactDetails_email', 'contactDetails_faxNumber', 'contactDetails_faxNumberAreaCode',
                  'contactDetails_faxNumberCountryCode', 'contactDetails_faxNumberSubscriber',
                  'contactDetails_firstname', 'contactDetails_homepageUrl', 'contactDetails_lastname',
                  'contactDetails_phoneNumber', 'contactDetails_phoneNumberAreaCode',
                  'contactDetails_phoneNumberCountryCode', 'contactDetails_phoneNumberSubscriber',
                  'contactDetails_salutation']

realEstateDetails = ['id', 'realEstate_id', 'realEstate_xsi_type', 'realEstate_address_city',
                     'realEstate_address_geoHierarchy_city_fullGeoCodeId',
                     'realEstate_address_geoHierarchy_city_geoCodeId', 'realEstate_address_geoHierarchy_city_name',
                     'realEstate_address_geoHierarchy_continent_fullGeoCodeId',
                     'realEstate_address_geoHierarchy_continent_geoCodeId',
                     'realEstate_address_geoHierarchy_country_fullGeoCodeId',
                     'realEstate_address_geoHierarchy_country_geoCodeId',
                     'realEstate_address_geoHierarchy_country_name',
                     'realEstate_address_geoHierarchy_neighbourhood_geoCodeId',
                     'realEstate_address_geoHierarchy_quarter_fullGeoCodeId',
                     'realEstate_address_geoHierarchy_quarter_geoCodeId',
                     'realEstate_address_geoHierarchy_quarter_name',
                     'realEstate_address_geoHierarchy_region_fullGeoCodeId',
                     'realEstate_address_geoHierarchy_region_geoCodeId',
                     'realEstate_address_geoHierarchy_region_name', 'realEstate_address_postcode',
                     'realEstate_address_quarter']
contactFormDetails = ['id', 'contactFormConfiguration_addressField',
                      'contactFormConfiguration_applicationPackageCompletedField',
                      'contactFormConfiguration_emailAddressField',
                      'contactFormConfiguration_employmentRelationshipField',
                      'contactFormConfiguration_firstnameField',
                      'contactFormConfiguration_freemiumSettings_duration', 'contactFormConfiguration_incomeField',
                      'contactFormConfiguration_lastnameField', 'contactFormConfiguration_messageField',
                      'contactFormConfiguration_moveInDateField', 'contactFormConfiguration_numberOfPersonsField',
                      'contactFormConfiguration_petsInHouseholdField', 'contactFormConfiguration_phoneNumberField',
                      'contactFormConfiguration_premiumProfileRequired', 'contactFormConfiguration_salutationField']
realEstateTitle = ['id', 'realEstate_title', 'realEstate_titlePicture_creation', 'realEstate_titlePicture_id',
                   'realEstate_titlePicture_modification', 'realEstate_titlePicture_publishDate',
                   'realEstate_titlePicture_floorplan', 'realEstate_titlePicture_title',
                   'realEstate_titlePicture_titlePicture', 'realEstate_titlePicture_urls']

fact_flat = ['id', 'creation', 'contactFormType', 'modification', 'publishDate', 'companyWideCustomerId',
             'realEstate_apartmentType', 'realEstate_assistedLiving', 'realEstate_attachments',
             'realEstate_balcony', 'realEstate_baseRent', 'realEstate_buildingEnergyRatingType',
             'realEstate_builtInKitchen', 'realEstate_calculatedTotalRent', 'realEstate_calculatedTotalRentScope',
             'realEstate_cellar', 'realEstate_certificateOfEligibilityNeeded', 'realEstate_condition',
             'realEstate_constructionYear', 'realEstate_courtage_hasCourtage', 'realEstate_creationDate',
             'realEstate_deposit', 'realEstate_descriptionNote',
             'realEstate_energyCertificate_energyCertificateAvailability',
             'realEstate_energyCertificate_energyCertificateCreationDate',
             'realEstate_energyConsumptionContainsWarmWater', 'realEstate_energyPerformanceCertificate',
             'realEstate_externalId', 'realEstate_floor', 'realEstate_floorplan', 'realEstate_freeFrom',
             'realEstate_furnishingNote', 'realEstate_garden', 'realEstate_guestToilet',
             'realEstate_handicappedAccessible', 'realEstate_heatingCosts',
             'realEstate_heatingCostsInServiceCharge', 'realEstate_heatingType', 'realEstate_heatingTypeEnev2014',
             'realEstate_interiorQuality', 'realEstate_lastModificationDate', 'realEstate_lastRefurbishment',
             'realEstate_lift', 'realEstate_livingSpace', 'realEstate_locationNote', 'realEstate_numberOfFloors',
             'realEstate_numberOfRooms', 'realEstate_otherNote', 'realEstate_petsAllowed',
             'realEstate_referencePriceApiCall', 'realEstate_referencePriceServiceCall', 'realEstate_serviceCharge',
             'realEstate_state', 'realEstate_thermalCharacteristic', 'realEstate_totalRent',
             'realEstate_useAsFlatshareRoom', 'realtorValuationJSONLink_xlink_href',
             'realtorValuationV2JSONLink_xlink_href', 'realtorValuationV2JSONPLink_xlink_href', 'xlink_href',
             'adLinkForJSONP_xlink_href', 'adLinkForXMLData_xlink_href', 'imprintLink_xlink_href']


def load_tables():
    md=RentData()
    md.input_filename=filename
    md.load_data_from_file()


    ## load contact_details Table
    md.export_to_file(contactDetails,'contact_details')
    md.postgres_data_load('temp.contact_details',md.filename,'Y','|')
    md.target_data_load('data_export.contact_details','id')


    ## load realestate_details Table
    md.export_to_file(realEstateDetails,'realestate_details')
    md.postgres_data_load('temp.realestate_details',md.filename,'Y','|')
    md.target_data_load('data_export.realestate_details','id')


    ##load contact_form_config Table
    md.export_to_file(contactFormDetails,'contact_form_config')
    md.postgres_data_load('temp.contact_form_config',md.filename,'Y','|')
    md.target_data_load('data_export.contact_form_config','id')


    ##load realEstateTitle Table
    md.export_to_file(realEstateTitle,'realEstateTitle')
    md.postgres_data_load('temp.realestate_title',md.filename,'Y','|')
    md.target_data_load('data_export.realestate_title','id')


    ##load fact_flat Table
    md.export_to_file(fact_flat, 'fact_flat', '|')
    md.postgres_data_load('temp.fact_flat', md.filename, 'Y', '|')
    md.target_data_load('data_export.fact_flat', 'id')
    del md



s3_file,filename=download_file()
load_tables()
s3_move_file(os.environ['S3_BUCKET'],s3_file)
