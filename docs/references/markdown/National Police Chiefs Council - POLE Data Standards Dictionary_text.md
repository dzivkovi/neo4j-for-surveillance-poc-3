[Image]

[Image]

## Minimum POLE Data Standards Dictionary

Prepared for

:

National Police Chiefs Council

Written by :

PDS &amp; Chaucer Group

Date :

30/07/2023

Version :

1.1 FINAL

[Image]

## Table of Contents

| 1.  Introduction  ...........................................................................................................................................................  4   | 1.  Introduction  ...........................................................................................................................................................  4   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1.1:                                                                                                                                                                               | Data Quality Dimensions ..................................................................................................................................  4                      |
| 1.2:                                                                                                                                                                               | POLE Entity Description  ....................................................................................................................................  5                   |
| 1.2.1:                                                                                                                                                                             | Data Components  .............................................................................................................................................  5                  |
| 1.2.2:                                                                                                                                                                             | Validation Rules  ................................................................................................................................................  6              |
| 1.3:                                                                                                                                                                               | Data Standards Descriptions ............................................................................................................................  7                        |
| 1.4:                                                                                                                                                                               | General Validation Notes .................................................................................................................................  8                      |
| 2.  Minimum Data Standards for PERSON Entities ...................................................................................................  10                             | 2.  Minimum Data Standards for PERSON Entities ...................................................................................................  10                             |
| 2.1:                                                                                                                                                                               | Offender .........................................................................................................................................................  10             |
| 2.2:                                                                                                                                                                               | Suspect - Known .............................................................................................................................................  12                  |
| 2.3:                                                                                                                                                                               | Suspect - Unknown  .........................................................................................................................................  14                   |
| 2.4:                                                                                                                                                                               | Victim  ..............................................................................................................................................................  16         |
| 2.5:                                                                                                                                                                               | Witness ...........................................................................................................................................................  18            |
| 2.6:                                                                                                                                                                               | Person of Interest - Known  .............................................................................................................................  20                      |
| 2.7:                                                                                                                                                                               | Person of Interest - Unknown ........................................................................................................................  22                          |
| 2.8:                                                                                                                                                                               | Subject (Not Offender, Victim or Witness)  .....................................................................................................  23                               |
| 2.9:                                                                                                                                                                               | Vulnerable Child .............................................................................................................................................  24                 |
| 2.10:                                                                                                                                                                              | Vulnerable Adult  .............................................................................................................................................  26                |
| 2.11:                                                                                                                                                                              | Unborn  ............................................................................................................................................................  28           |
| 2.12:                                                                                                                                                                              | Involved Party  .................................................................................................................................................  30              |
| 2.13:                                                                                                                                                                              | Associations ....................................................................................................................................................  31              |
| 2.14:                                                                                                                                                                              | Missing Persons ..............................................................................................................................................  33                 |
| 2.15:                                                                                                                                                                              | Officer on Duty ...............................................................................................................................................  35                |
| 2.16:                                                                                                                                                                              | Victim whilst on Duty .....................................................................................................................................  36                    |
| 2.17:                                                                                                                                                                              | Person Reporting / Organisation  ....................................................................................................................  37                          |
| 2.18:                                                                                                                                                                              | Person Reporting / General Public .................................................................................................................  38                            |
| 2.19:                                                                                                                                                                              | Sudden Death / No Crime / Non-suspicious  ...................................................................................................  39                                  |
| 2.20:                                                                                                                                                                              | Sudden Death / Victim / Unexplained  ............................................................................................................  41                              |

[Image]

| 3.  Minimum Data Standards for OBJECT Entities ....................................................................................................  43   | 3.  Minimum Data Standards for OBJECT Entities ....................................................................................................  43                   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 3.1:                                                                                                                                                      | Vehicle Known ................................................................................................................................................  43        |
| 3.2:                                                                                                                                                      | Vehicle Suspicious ..........................................................................................................................................  44         |
| 3.3:                                                                                                                                                      | Telephone  .......................................................................................................................................................  45    |
| 3.4:                                                                                                                                                      | Email ...............................................................................................................................................................  46 |
| 3.5:                                                                                                                                                      | Passport ..........................................................................................................................................................  47   |
| 3.6:                                                                                                                                                      | Driving Licence  ................................................................................................................................................  48     |
| 3.7:                                                                                                                                                      | CRO Number ...................................................................................................................................................  49        |
| 3.8:                                                                                                                                                      | PNC ID  .............................................................................................................................................................  50 |
| 3.9:                                                                                                                                                      | NI Number ......................................................................................................................................................  51      |
| 3.10:                                                                                                                                                     | Property  ..........................................................................................................................................................  52  |
| 3.11:                                                                                                                                                     | Custody Image ................................................................................................................................................  53        |
| 3.12:                                                                                                                                                     | Photograph .....................................................................................................................................................  54      |
| 3.13:                                                                                                                                                     | Unique Social Media Tag ................................................................................................................................  55              |
| 4.  Minimum Data Standards for LOCATION Entities ...............................................................................................  56      | 4.  Minimum Data Standards for LOCATION Entities ...............................................................................................  56                      |
| 4.1:                                                                                                                                                      | Residential Address ........................................................................................................................................  56          |
| 4.2:                                                                                                                                                      | Business Address ............................................................................................................................................  58         |
| 4.3:                                                                                                                                                      | Location - Geometric ......................................................................................................................................  59           |
| 4.4:                                                                                                                                                      | Location - Area................................................................................................................................................  60       |
| 4.5:                                                                                                                                                      | Location - NFA ................................................................................................................................................  61       |
| 5.                                                                                                                                                        | Minimum Data Standards for EVENT Entities......................................................................................................  62                       |
| 5.1:                                                                                                                                                      | Crime ..............................................................................................................................................................  62  |
| 5.2:                                                                                                                                                      | Incident  ...........................................................................................................................................................  65 |
| 5.3:                                                                                                                                                      | Custody  ...........................................................................................................................................................  67  |
| 5.4:                                                                                                                                                      | Stop Search  .....................................................................................................................................................  69    |
| 5.5:                                                                                                                                                      | Safeguarding  ...................................................................................................................................................  71     |
| 5.6:                                                                                                                                                      | Anti-social Behaviour  ......................................................................................................................................  73         |
| 6.                                                                                                                                                        | POLE Data Attribute Standards ...........................................................................................................................  79             |
| 7.                                                                                                                                                        | References .........................................................................................................................................................  137 |

[Image]

## 1. Introduction

This compendium has been produced to support the consistent and accurate recording of police operational information and data. It is intended to be used to inform quality performance management at a local level, technical developments across main suppliers, data validation at the point of creation and tailored learning for those responsible for inputting data.

These standards apply to all officers, staff, PCSOs, Special Constables and volunteers.

This set of standards has been organised around POLE (Person, Object, Location, Event) entities. It identifies the minimum required completion standard and will flag any required formatting. It also includes a set of 'Key Data Quality Points' - See General Validation Notes.

Where possible this document is system agnostic. It is acknowledged that there may be differences between systems in the terminology used and differences between Forces in how systems are utilised. Nuances between systems should be coordinated to ensure all Forces are aware and working towards a consistent standard. The aim is to avoid, where possible, Forces determining standards with no regard for national implications.

It is up to each Force to determine how best to incorporate these standards into business-as-usual data recording - and it is accepted that this will be determined in some part by cost and resource availability. Data uploaded to national systems will be assessed against these standards and Forces will be provided with an assessment of their data and the URN of those records that have failed to meet the standard.

This Dictionary does not detail association rules between entities.

This Dictionary does not serve to construct a data structure but to define the minimum standards for entities.

This is seen as the first step to defining full set of data standards.

## 1.1: Data Quality Dimensions

Data Quality is defined by the following data quality dimensions:

- -Accuracy. Data should be sufficiently accurate for its intended purpose - correctly reflecting the object
- -Integrity. Data is valid across all relationships and is used in compliance with relevant requirements
- -Timeliness. Data should be captured as quickly as possible after the event and should be available when it is expected and needed
- -Completeness. Data meets expected comprehensiveness. Completeness measures if the data is sufficient to deliver meaningful inferences and decisions. For example, if the person's address includes an optional landmark attribute, data can be considered complete even when the landmark information is missing.'

[Image]

- -Conformity. Data follows a set standard of definitions and reflects stable and consistent data collection processes
- -Duplication. Data is unique and should be captured only once to minimise error and maximise benefit

## 1.2: POLE Entity Description

Data entities are constructed from a combination of 'data components' and 'validation rules'. They describe people, objects, and locations associated with events - see Figure 1.

Figure 1: POLE

[Image]

## 1.2.1: Data Components

NOTE: Data components listed in this Data Dictionary provide the minimum components required to describe the associated POLE entity.

Each data component is defined in one of three ways:

- -Unique Data Standard - The data component is defined by a specific data standard. The data component may be used in multiple entities, but it is always defined in the same way and, by the same data standard (e.g. DS\_032 Surname)
- -Local Data Standard - The data component is defined by a 'generic' data standard that has 'local'
- validation rules applied. The data component may be used in multiple entities, but it is always defined by the same 'generic' data standard with the same 'locally' applicable validation rules. (e.g. 'Date of Birth' is an instance of DS\_001 Generic Date with validation rules applied, such as 'Date not
- in the future' and it is described as 'the date a person is deemed officially to have been born on')

[Image]

- -Entity - The data component is an instance of another entity and will be defined by the relevant data standards of that entity.

(eg 'Home Address' is built from a collection of instances ' Address (DS\_005, DS\_007, DS\_008, DS\_009, DS\_010) '). There may also be additional 'local' validation rules that are applied for this specific data component.

Data components can be repeated / used separately for multiple entities.

## 1.2.2: Validation Rules

Validation rules 'specify' the requirements for any particular entity (eg the 'Victim' Entity within the 'Person' Entity class):

- -Validation rules may apply to a selection of data components - eg their status (eg These data components are mandatory)
- -Specific validation rules can be applied to particular data components that will help define them, in the particular entity.

Table 1 describes the descriptors used in Entity definitions in Section 2.

| Data Item        | Description                                                                                                                                                                                                |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Reference Number | Y_XXX  Reference number for Each Entity.  Y = Entity Class: P = Person; O = Object; L = Location; E = Event  XXX = Serial Number                                                                           |
| Entity           | Entity title                                                                                                                                                                                               |
| Class            | Class title (Person, Object, Location, Event)                                                                                                                                                              |
| Owner            | The name of the organisation which owns the Entity                                                                                                                                                         |
| Steward          | The organisation who maintains the Entity on behalf of the owner                                                                                                                                           |
| Version          | Number indicating the particular revision of the Entity                                                                                                                                                    |
| Status           | Draft / Live / Deprecated                                                                                                                                                                                  |
| Approval Date    | The date on which the current version of the entity was approved at a meeting of  National Standards Assurance Board (NSAB)                                                                                |
| Description      | Textual explanation of the entity in terms of  what  the entity is, its intended  purpose and the context in which it may be used.                                                                         |
| Component Parts  | The minimum list of data components and their descriptions that compose the  entity describing whether they are mandatory, dependent on certain conditions,  or options of which one or more are required. |

[Image]

Table 1: Entity element descriptors

| Validation Rules   | The rules that apply to the entity and its components in terms of syntax and  structure.   |
|--------------------|--------------------------------------------------------------------------------------------|
| Related Terms      | TBC                                                                                        |
| Notes              | TBC                                                                                        |

## 1.3: Data Standards Descriptions

Data components are ultimately defined by data standards either directly or with the application of additional validation rules within the entity.

Data standards can be specific or generic - regardless of type, they are constructed in the same way.

Table 2 describes the elements for a data standard as described in Section 6.

| Data Item             | Descriptor                                                                                                                                                                                         |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SERIAL NO             | Unique reference number to identify and locate POLE data standard                                                                                                                                  |
| POLE Class            | Class title (Person, Object, Location, Event)                                                                                                                                                      |
| Entity Group          | Attributes are grouped under common headings                                                                                                                                                       |
| Attribute Name        | Data Attribute title                                                                                                                                                                               |
| Attribute Description | A textual account, explanation or representation of a Structure in terms  of what the structure is, its intended purpose and the context in which  it may be used.                                 |
| Version               | Number indicating the particular revision of the data attribute                                                                                                                                    |
| Approval Date         | The date on which the current version of the data attribute was  approved at a meeting of National Standards Assurance Board (NSAB)                                                                |
| Minimum               | The minimum number of characters that must be used for an Element's  value.                                                                                                                        |
| Maximum               | The maximum number of characters that maybe used for an Element's  value.                                                                                                                          |
| Default               | The default value is the value which is to be used unless some other  value has been actively selected from the set of allowable values; see  Values below                                         |
| Value Range           | If not free text this field describes the set of possible values for this data  attribute                                                                                                          |
| Validation            | Any validation rules that are needed for this data attribute are  described in this field. This may include character types, formats,  allowed or disallowed character sets and combinations etc.. |

[Image]

Table 2: Data Standards and Elements

| Standard Classification   | International = International standard  National = National standard exists  Police National to be agreed - Policing need to agree consistent set of  standards  N/A - not applicable   Free text = Force data input  System generated standard = system generated code   |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board                     | The name(s) of the organisation which owns the Structure                                                                                                                                                                                                                  |
| Owner                     | The name(s) of the organisation/business area which owns the  standard                                                                                                                                                                                                    |
| Steward                   | The organisation / organisational unit who maintains the Structure on  behalf of the Owner of that Structure.                                                                                                                                                             |
| Based on                  | Formats and standards for each data attribute where possible have  been based on existing standards and guidance. If this is the case that  source is listed in this field.                                                                                               |
| Data source               | Any data sources or further clarification / notes are given in this field                                                                                                                                                                                                 |
| Minimum STANDARD          | Yes = Standard referenced as Minimum POLE Data Standards                                                                                                                                                                                                                  |
| Protected characteristic  | YES = link to Protected Characteristics (Under the Equality Act, there are  nine protected characteristics:  age  disability  gender reassignment  marriage and civil partnership  pregnancy and maternity  race  religion or belief  sex                                 |

## 1.4: General Validation Notes

The following 'dos and don'ts' are given as general advice in the adoption of these data standards:

-  Expected comprehensiveness of person records is always determined by the relationship a person has to the event to which they are linked.  One would expect a more complete set of person-identifying data on a known offender than a suspect.
-  If a person entity is created, it must conform to the minimum data standards defined in Section 2. If the 4+1 (Given Name, Surname, Date of Birth, Gender + Some form of contact reference) criteria are not known at the point of entry, they should be completed as soon as possible following contact with the police.

[Image]

-  A person should not be created if there is no person identifying data or physical attributes. This includes where the details of a victim (4+1) are unknown.
-  Any standard address details must include a valid and accurate postcode.  Unconfirmed and/or fictitious postcodes are not to be created at any time and every effort must be made to identify the correct postcode.
-  Postcodes should comply with the national Royal Mail Postcode Address File which not only confirms the format (area, district, sector, unit), but also validates against the address.
-  There is no expectation to capture a postcode for a non-standard address e.g. a field or road junction.
-  Telephone numbers should include any area dialling code - numbers without a dialling code are almost meaningless when shared nationally.
-  If a telephone number is unknown - do not make one up.
-  Always check the date of birth - ensuring you follow the dd/mm/yyyy format.
-  Always check any dates and ensure dates are input into the correct/relevant field.  Common mistakes include: inputting the arrest date in the date of birth field; event dates in the future.
-  Always ask the spelling of names - enter what is known and not what is assumed.
-  Ensure that any person entity is linked to one or more additional entity.  Orphan records do not comply with key Data Protection principles.
-  Any titles such as Dr must not be added to the forename field - titles should always be selected from the drop-down title menu if available.
-  Do not use local landmarks and/or local references to populate address/location information.
-  Do not populate fields with special characters when the field is unknown.  A blank field is preferable to a known error; however, every effort should be made to enter a complete record where possible.
-  Do not populate records with local vernacular and abbreviations - this makes it very difficult to understand the context of a record when shared with partners or uploaded to the Police National Database.
-  Do not use local references in person identifying fields - for example incident reference in a forename field when a name is unknown.
-  Do not populate a names field with multiple names - the only exception being double barrelled.
-  Do not use special characters in a name field - exceptions are hyphens, apostrophes.
-  Animals should be recorded as property, not as people.
-  Any graffiti hashtags containing special characters should be input into the alias/nickname field.
-  Never create a business/organisation entity as a person record - Mr Tesco Express is not a person.

[Image]

## 2. Minimum Data Standards for PERSON Entities

If a person entity is created, it must conform to the minimum data standards defined. If the 4+1 criteria is not known at the point of entry it should be completed as soon as possible following police contact.  A person should not be created if there is no person identifying data or physical attributes. This includes where the details of a victim (4+1) are unknown.

## 2.1: Offender

| Ref No:   | P_001   | Entity   | Offender   | Offender        |
|-----------|---------|----------|------------|-----------------|
| Class:    | Person  | Owner:   |            | Steward:        |
| Version:  |         | Status:  | Draft      | Approval  Date: |

## Minimum Completeness Requirement

| Description   | An offender is a person who has been charged, reported, cautioned, fined, warned or  received a restorative justice or some other out of court disposal for their involvement  in an offence.   | An offender is a person who has been charged, reported, cautioned, fined, warned or  received a restorative justice or some other out of court disposal for their involvement  in an offence.   |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component     | 1. The following component parts are mandatory:                                                                                                                                                 | 1. The following component parts are mandatory:                                                                                                                                                 |
| Component     | Given Name                                                                                                                                                                                      | DS_031 Given Name                                                                                                                                                                               |
| Component     | Surname                                                                                                                                                                                         | DS_032 Surname                                                                                                                                                                                  |
| Component     | Date of Birth                                                                                                                                                                                   | DS_034 Date of Birth                                                                                                                                                                            |
| Component     | Age                                                                                                                                                                                             | DS_120 Age                                                                                                                                                                                      |
| Component     | Gender                                                                                                                                                                                          | DS_037 Gender                                                                                                                                                                                   |
| Parts         | 2. At least one of the following contact references must be included:                                                                                                                           | 2. At least one of the following contact references must be included:                                                                                                                           |
| Parts         | Home Address                                                                                                                                                                                    | This is the self-declared home address  This is an instance of  Address (DS_005, DS_007,  DS_008, DS_009, DS_010)                                                                               |
| Parts         | Telephone Number                                                                                                                                                                                | DS_053 Telephone Number                                                                                                                                                                         |
| Parts         | Email Address                                                                                                                                                                                   | DS_054 Email Address                                                                                                                                                                            |

[Image]

|                   | CRO Number  DS_071 CRO Number  PNC ID  DS_072 PNC ID                                                                                                                                                                                                                                                                                                        |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation  Rules | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name  2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number  3. Email Address  can repeat as a Person can have multiple occurrences of an  email address  4.  Age  Date of birth  5. See Component Standards for all components. |
| Related  Terms    |                                                                                                                                                                                                                                                                                                                                                             |
| Notes             |  See General Validation Notes                                                                                                                                                                                                                                                                                                                              |

Description

## Component

Parts

[Image]

## 2.2: Suspect - Known

| Ref No:   | P_002   | Entity   | Suspect - Known   | Suspect - Known   |
|-----------|---------|----------|-------------------|-------------------|
| Class:    | Person  | Owner:   |                   | Steward:          |
| Version:  |         | Status:  | Draft             | Approval  Date:   |

## Minimum Completeness Requirement

A Known Suspect identified by the police, or other authority as having sufficient, reasonable, and objective grounds to suspect them of committing an offence.

There must be some reasonable, objective grounds for the suspicion, based on known facts or information which are relevant to the likelihood the offence has been committed and the person to be questioned committed it.

The identity of the suspect being 'known' means that there is sufficient information known to the police to establish that there are reasonable grounds to suspect a particular person of involvement in the offence.

A suspect can be used for the recording of a non-notifiable offence as well as a crime.

4. The following component parts are mandatory:
5. At least one of the following contact references must be included:

Given Name

DS\_031 Given Name

Surname

DS\_032 Surname

Date of Birth

DS\_034 Date of Birth

Age

DS\_120 Age

Gender

DS\_037 Gender

Home Address

This is the self-declared home address

This is an instance of Address (DS\_005, DS\_007,

DS\_008, DS\_009, DS\_010)

Telephone Number Email Address

DS\_053 Telephone Number

DS\_054 Email Address

[Image]

|                   | 1 Given Name  repeats as a Person can have multiple occurrences of a given  name  2 Telephone Number  can repeat as a Person can have multiple occurrences   |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation  Rules | of a telephone number  3 Email Address                                                                                                                       |
|                   | can repeat as a Person can have multiple occurrences of an  email address                                                                                    |
|                   | 4 See Component Standards for all components.                                                                                                                |
| Related  Terms    |  Suspect - Unknown                                                                                                                                          |
| Notes             |  See General Validation Notes                                                                                                                               |

[Image]

## 2.3: Suspect - Unknown

| Ref No:   | P_003   | Entity   | Suspect - Unknown   | Suspect - Unknown   | Suspect - Unknown   |
|-----------|---------|----------|---------------------|---------------------|---------------------|
| Class:    | Person  | Owner:   |                     | Steward:            |                     |
| Version:  |         | Status:  | Draft               | Approval  Date:     |                     |

## Minimum Completeness Requirement

| Description       | An 'unknown' suspect is a description of a suspect believed by the authorities  to have committed a crime but whose personal details are not yet known. As  such only certain physical attributes can be used to define the unknown  suspect.                                                                                           | An 'unknown' suspect is a description of a suspect believed by the authorities  to have committed a crime but whose personal details are not yet known. As  such only certain physical attributes can be used to define the unknown  suspect.                                                                                           |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component         | 1. At least 4 of the following component parts must be included:                                                                                                                                                                                                                                                                        | 1. At least 4 of the following component parts must be included:                                                                                                                                                                                                                                                                        |
| Parts             | Gender  Build  Complexion  Distinguishing Features  Eye Colour - Left  Eye Colour - Right  Ethnicity                                                                                                                                                                                                                                    | DS_037 Gender  DS_039 Build  DS_040 Complexion  DS_043 Distinguishing Features  DS_041 Eye Colour Left  DS_042 Eye Colour Right  DS_038 Ethnicity                                                                                                                                                                                       |
| Validation  Rules | 1. See Component Standards for all components.                                                                                                                                                                                                                                                                                          | 1. See Component Standards for all components.                                                                                                                                                                                                                                                                                          |
| Related  Terms    |  Suspect - Known                                                                                                                                                                                                                                                                                                                       |  Suspect - Known                                                                                                                                                                                                                                                                                                                       |
| Notes             |  See General Validation Notes   Data items  DS_039-46  above are classed as biometric data -  information about an individual's physical, biological, physiological or  behavioural characteristics, which is capable of being used on its own  or in combination with other information to establish the identity of an  individual. |  See General Validation Notes   Data items  DS_039-46  above are classed as biometric data -  information about an individual's physical, biological, physiological or  behavioural characteristics, which is capable of being used on its own  or in combination with other information to establish the identity of an  individual. |

[Image]

[Image]

## 2.4: Victim

| Ref No:   | P_004   | Entity   | Victim   | Victim          | Victim   |
|-----------|---------|----------|----------|-----------------|----------|
| Class:    | Person  | Owner:   |          | Steward:        |          |
| Version:  |         | Status:  | Draft    | Approval  Date: |          |

## Minimum Completeness Requirement

Description

The Code of Practice for Victims of Crime in England and Wales, November 2020 defines a victim as:

-  A victim is a person who has suffered harm, including physical, mental or emotional harm or economic loss which was directly caused by a criminal offence; a close relative (or a nominated family spokesperson) of a person whose death was directly caused by a criminal offence.

Component

Parts

1. The following component parts are mandatory:

Given Name

DS\_031 Given Name

Surname

DS\_032 Surname

Date of Birth

DS\_034 Date of Birth

Age

DS\_120 Age

Gender

DS\_037 Gender

2. At least one of the following contact references must be included:

Home Address

This is the self-declared home address

This is an instance of Address (DS\_005, DS\_007,

DS\_008, DS\_009, DS\_010)

Telephone Number Email Address

DS\_053 Telephone Number

DS\_054 Email Address

## Validation Rules

1. Given Name can repeat as a Person can have multiple occurrences of a given name

2. Telephone Number can repeat as a Person can have multiple occurrences of a telephone number

3. Email Address can repeat as a Person can have multiple occurrences of an email address

[Image]

|                | 4. See Component Standards for all components.   |
|----------------|--------------------------------------------------|
| Related  Terms |                                                  |
| Notes          |  See General Validation Notes                   |

[Image]

## 2.5: Witness

| Ref No:   | P_005   | Entity   | Witness   |                 |
|-----------|---------|----------|-----------|-----------------|
| Class:    | Person  | Owner:   |           | Steward:        |
| Version:  |         | Status:  | Draft     | Approval  Date: |

## Minimum Completeness Requirement

Description

A witness is a person, other than a defendant, who may be called to provide evidence that is material to the offence being heard or a non-crime event.

Whilst all victims are also witnesses and should be treated as such, details for victims should be captured as part of the 'Victim' entity.

Black's Law dictionary 2 nd edition defines a witness as 1. Person who sees a document signed. 2. Person called to court to testify and give evidence.

## Component Parts

1. The following component parts are mandatory:

Given Name

DS\_031 Given Name

Surname

DS\_032 Surname

Date of Birth

DS\_034 Date of Birth

Age

DS\_120 Age

Gender

DS\_037 Gender

2. At least one of the following contact references must be included:

Home Address

This is the self-declared home address

This is an instance of Address (DS\_005, DS\_007,

DS\_008, DS\_009, DS\_010)

Telephone Number Email Address

DS\_053 Telephone Number

DS\_054 Email Address

## Validation Rules

1. Given Name can repeat as a Person can have multiple occurrences of a given name

2. Telephone Number can repeat as a Person can have multiple occurrences of a telephone number

3. Email Address can repeat as a Person can have multiple occurrences of an email address

[Image]

|                | 4. See Component Standards for all components.   |
|----------------|--------------------------------------------------|
| Related  Terms |                                                  |
| Notes          |  See General Validation Notes                   |

[Image]

## 2.6: Person of Interest - Known

| Ref No:   | P_006   | Entity   | Person of Interest - Known   | Person of Interest - Known   |
|-----------|---------|----------|------------------------------|------------------------------|
| Class:    | Person  | Owner:   |                              | Steward:                     |
| Version:  |         | Status:  | Draft                        | Approval  Date:              |

## Minimum Completeness Requirement

## Description

A Person of Interest is an identified person considered by police to be linked to an investigation, who would not need to be cautioned (as per PACE 1984 Code C) by police.

They could be a person who is cooperating with the investigation, may have information that would assist the investigation, or possess certain characteristics that merit further attention.

## Component

Parts

1. The following component parts are mandatory:

Given Name

DS\_031 Given Name

Surname

DS\_032 Surname

Date of Birth

DS\_034 Date of Birth

Age

DS\_120 Age

Gender

DS\_037 Gender

2. At least one of the following contact references must be included:

Home Address

This is the self-declared home address

This is an instance of Address (DS\_005, DS\_007,

DS\_008, DS\_009, DS\_010)

Telephone Number Email Address Alias / Nickname

DS\_053 Telephone Number

DS\_054 Email Address

DS\_033 Alias / Nickname

## Validation Rules

1. Given Name can repeat as a Person can have multiple occurrences of a given name

2. Telephone Number can repeat as a Person can have multiple occurrences of a telephone number

3. Email Address can repeat as a Person can have multiple occurrences of an email address

[Image]

|                | 4. Alias / Nickname  can repeat as a Person can have multiple occurrences of  an alias / nickname  5. Alias / nickname  should  not  be captured in the  Given Name  component  6. See Component Standards for all components.   |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Related  Terms |  Person of Interest - Unknown                                                                                                                                                                                                   |
| Notes          |  See General Validation Notes                                                                                                                                                                                                   |

[Image]

## 2.7: Person of Interest - Unknown

| Ref No:   | P_007   | Entity   | Person of Interest - Unknown   | Person of Interest - Unknown   |
|-----------|---------|----------|--------------------------------|--------------------------------|
| Class:    | Person  | Owner:   |                                | Steward:                       |
| Version:  |         | Status:  | Draft                          | Approval  Date:                |

## Minimum Completeness Requirement

| An unknown Person of Interest is an unidentified person considered by police                                                                                                                                                                                                                                                                                                                                                    | An unknown Person of Interest is an unidentified person considered by police                                                                                                                                                                                                                                                                                                                                                    |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description  to be linked to an investigation, who would not need to be cautioned (as per  PACE 1984 Code C) by police.  They could be a person who is cooperating with the investigation, may have  information that would assist the investigation or possess certain  characteristics that merit further attention but whose details are not fully  known.  1. At least 4 of the following component parts must be included: | Description  to be linked to an investigation, who would not need to be cautioned (as per  PACE 1984 Code C) by police.  They could be a person who is cooperating with the investigation, may have  information that would assist the investigation or possess certain  characteristics that merit further attention but whose details are not fully  known.  1. At least 4 of the following component parts must be included: |
| Gender  Build  Complexion  Distinguishing Features  Eye Colour - Left  Eye Colour - Right  Ethnicity  Hair Colour                                                                                                                                                                                                                                                                                                               | DS_037 Gender  DS_039 Build  DS_040 Complexion  DS_043 Distinguishing Features  DS_041 Eye Colour Left  DS_042 Eye Colour Right  DS_038 Ethnicity  DS_046 Hair Colour                                                                                                                                                                                                                                                           |
| Validation  Rules  1. Alias / Nickname  can repeat as a Person can have multiple occurrences of  an alias / nickname  2. Alias / nickname  should  not  be captured in  Given Name  component                                                                                                                                                                                                                                   | Validation  Rules  1. Alias / Nickname  can repeat as a Person can have multiple occurrences of  an alias / nickname  2. Alias / nickname  should  not  be captured in  Given Name  component                                                                                                                                                                                                                                   |
| Related  Terms   Person of Interest - Known                                                                                                                                                                                                                                                                                                                                                                                    | Related  Terms   Person of Interest - Known                                                                                                                                                                                                                                                                                                                                                                                    |
| Notes   See General Validation Notes                                                                                                                                                                                                                                                                                                                                                                                           | Notes   See General Validation Notes                                                                                                                                                                                                                                                                                                                                                                                           |

[Image]

## 2.8: Subject (Not Offender, Victim or Witness)

| Ref No:   | P_008   | Entity   | Subject (Not Offender, Victim or Witness)   | Subject (Not Offender, Victim or Witness)   | Subject (Not Offender, Victim or Witness)   |
|-----------|---------|----------|---------------------------------------------|---------------------------------------------|---------------------------------------------|
| Class:    | Person  | Owner:   |                                             | Steward:                                    |                                             |
| Version:  |         | Status:  | Draft                                       | Approval  Date:                             |                                             |

## Minimum Completeness Requirement

|                  | A subject is a person who cannot be categorised as an offender, suspect, victim,  witness or person of interest because their role is based on an intelligence  source, and not based on material that could be submitted as evidence in open                                        | A subject is a person who cannot be categorised as an offender, suspect, victim,  witness or person of interest because their role is based on an intelligence  source, and not based on material that could be submitted as evidence in open                                        |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts | court.  1. The following component parts are mandatory:  2.                                                                                                                                                                                                                          | court.  1. The following component parts are mandatory:  2.                                                                                                                                                                                                                          |
| Rules            | Given Name  Surname  Date of Birth  Age  Gender  Home Address                                                                                                                                                                                                                        | DS_031 Given Name  DS_032 Surname  DS_034 Date of Birth DS_120 Age  DS_037 Gender  At least one of the following contact references must be included:  This is the self-declared home address                                                                                        |
| Validation       | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name   2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number  3. Email Address  can repeat as a Person can have multiple occurrences of an  email address | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name   2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number  3. Email Address  can repeat as a Person can have multiple occurrences of an  email address |
| Notes            |  See General Validation Notes                                                                                                                                                                                                                                                       |  See General Validation Notes                                                                                                                                                                                                                                                       |

[Image]

## 2.9: Vulnerable Child

| Ref No:   | P_009   | Entity   | Vulnerable Child   | Vulnerable Child   |
|-----------|---------|----------|--------------------|--------------------|
| Class:    | Person  | Owner:   |                    | Steward:           |
| Version:  |         | Status:  | Draft              | Approval  Date:    |

## Minimum Completeness Requirement

Description

A child is regarded as someone under 18 years of age. A child is always considered to be vulnerable, irrespective of the adult vulnerability criteria. A child may show mental, physical or learning disabilities or show illness, but this should be considered as an additional reporting factor reinforcing the child's inability to protect themselves against significant harm or exploitation.

(NCA Guidance on reporting routes relating to vulnerable persons)

## Component Parts

1. The following component parts are mandatory:

Given Name Surname Date of Birth Age Gender Home Address

DS\_031 Given Name

DS\_032 Surname

DS\_034 Date of Birth

DS\_120 Age

DS\_037 Gender

This is the self-declared home address

This is an instance of Address (DS\_005, DS\_007, DS\_008, DS\_009, DS\_010) DS\_031 Given Name (Parent / Legal Guardian) DS\_032 Surname (Parent / Legal Guardian)

Parent

DS\_047 Person Relationship

2. At least one of the following contact references must be included:

Telephone Number Email Address

DS\_053 Telephone Number

DS\_054 Email Address

Validation Rules

1. Given Name can repeat as a Person can have multiple occurrences of a given name

2. Telephone Number can repeat as a Person can have multiple occurrences of a telephone number

[Image]

|                | 3. Email Address  can repeat as a Person can have multiple occurrences of an  email address  4. See Component Standards for all components.   |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Related  Terms |  Vulnerable Adult                                                                                                                            |
| Notes          |  See General Validation Notes                                                                                                                |

Description

[Image]

## 2.10: Vulnerable Adult

| Ref No:   | P_010   | Entity   | Vulnerable Adult   | Vulnerable Adult   |
|-----------|---------|----------|--------------------|--------------------|
| Class:    | Person  | Owner:   |                    | Steward:           |
| Version:  |         | Status:  | Draft              | Approval  Date:    |

## Minimum Completeness Requirement

A vulnerable adult is any person aged 18 years or over who is or may be in need of community services by reason of mental, physical or learning disability, age or illness and is, or may be, unable to take care of themselves or unable to protect themselves against significant harm or exploitation.

Risks to vulnerable adults include (but are not limited to) sexual and other physical abuse, financial abuse (including fraud) and they may be the victims of modern slavery. The latter is defined in the Modern Slavery Act 2015, and means that it is a crime to force people into slavery, servitude and forced or compulsory labour.

(NCA Guidance on reporting routes relating to vulnerable persons)

A vulnerable adult is defined in Section 59 of the Safeguarding Vulnerable Groups Act 2006 (for England and Wales) as:

A person is a vulnerable adult if, having attained the age of 18, s/he -

1. is in residential accommodation,
2. is in sheltered housing,
3. receives domiciliary care,
4. receives any form of health care,
5. is detained in lawful custody,
6. by virtue of an order of a court, is under supervision per Criminal Justice Act 2003 sections regarding community sentences;
7. receives a welfare service of a prescribed description,
8. receives any service or participates in any activity provided specifically for persons who has particular needs because of his age, has any form

## Component

Parts

## Validation Rules

Related

Terms

Notes of disability or has a prescribed physical or mental problem (Dyslexia, dyscalculia and dyspraxia are excluded disabilities),

9. has payments made to him/her or to an accepted representative in pursuance of arrangements under Health and Social Care Act 2012, and/or
10. requires assistance in the conduct of own affairs.
1. The following component parts are mandatory:
2. At least one of the following contact references must be included:
3. If available the following component part should be included:

Given Name

DS\_031 Given Name

Surname

DS\_032 Surname

Date of Birth

DS\_034 Date of Birth

Age

DS\_120 Age

Gender

DS\_037 Gender

Home Address

This is the self-declared home address

This is an instance of Address (DS\_005, DS\_007, DS\_008, DS\_009, DS\_010)

Telephone Number

DS\_053 Telephone Number

Email Address

DS\_054 Email Address

Safe Number

## DS\_111 SAFE Number

1. Given Name can repeat as a Person can have multiple occurrences of a given name
2. Telephone Number can repeat as a Person can have multiple occurrences of a telephone number
3. Email Address can repeat as a Person can have multiple occurrences of an email address
4. See Component Standards for all components.
5.  Vulnerable Child
6.  See General Validation Notes

[Image]

[Image]

## 2.11: Unborn

| Ref No:   | P_011   | Entity   | Unborn   | Unborn          | Unborn   |
|-----------|---------|----------|----------|-----------------|----------|
| Class:    | Person  | Owner:   |          | Steward:        |          |
| Version:  |         | Status:  | Draft    | Approval  Date: |          |

## Minimum Completeness Requirement

| Description                    | An unborn person is a child in the womb.   Importantly this entity must be amended when the child is born to ensure that  duplicate records are not created.                                                                    | An unborn person is a child in the womb.   Importantly this entity must be amended when the child is born to ensure that  duplicate records are not created.                                                                    |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  Home Address | 1. The following component parts are mandatory:                                                                                                                                                                                 | This is the self-declared home address                                                                                                                                                                                          |
|                                | Mother Surname  Parent  Expected Due Date                                                                                                                                                                                       | The surname should be that of the mother  This is an instance of  DS_032 Surname  P_008 Subject (NOT offender, victim or witness) DS_003 Expected Due Date                                                                      |
|                                | 1. Expected Due Date  must not be in the past  2. Expected Due Date  must not be more than 9 months in the future  3. This entity should be edited when born. A new entity should not be created  as this will cause duplicates | 1. Expected Due Date  must not be in the past  2. Expected Due Date  must not be more than 9 months in the future  3. This entity should be edited when born. A new entity should not be created  as this will cause duplicates |
| Given Name  Gender             | DS_037 Gender                                                                                                                                                                                                                   | DS_031 Given Name                                                                                                                                                                                                               |
| Validation  Rules              | 3. If known, the following component parts should be included:                                                                                                                                                                  | 3. If known, the following component parts should be included:                                                                                                                                                                  |

[Image]

|                | 4. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number  5. Email Address  can repeat as a Person can have multiple occurrences of an  email address  6. See Component Standards for all components   |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Related  Terms |  Vulnerable Child                                                                                                                                                                                                                             |
| Notes          |  See General Validation Notes                                                                                                                                                                                                                 |

[Image]

## 2.12: Involved Party

| Ref No:   | P_012   | Entity   | Involved Party   | Involved Party   |
|-----------|---------|----------|------------------|------------------|
| Class:    | Person  | Owner:   |                  | Steward:         |
| Version:  |         | Status:  | Draft            | Approval  Date:  |

## Minimum Completeness Requirement

| Description       | An 'involved party' is someone who is involved with a wider situation, or has a  strong connection with it, such as a dependant or family member but not with  the actual event in question (if they were involved in the event they would be a  witness or victim).   | An 'involved party' is someone who is involved with a wider situation, or has a  strong connection with it, such as a dependant or family member but not with  the actual event in question (if they were involved in the event they would be a  witness or victim).   | An 'involved party' is someone who is involved with a wider situation, or has a  strong connection with it, such as a dependant or family member but not with  the actual event in question (if they were involved in the event they would be a  witness or victim).   |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                                                                                                                                                                                        | 1. The following component parts are mandatory:                                                                                                                                                                                                                        | 1. The following component parts are mandatory:                                                                                                                                                                                                                        |
| Component  Parts  | Given Name                                                                                                                                                                                                                                                             | DS_031 Given Name                                                                                                                                                                                                                                                      | DS_031 Given Name                                                                                                                                                                                                                                                      |
| Component  Parts  | Surname                                                                                                                                                                                                                                                                | DS_032 Surname                                                                                                                                                                                                                                                         | DS_032 Surname                                                                                                                                                                                                                                                         |
| Component  Parts  | Date of Birth                                                                                                                                                                                                                                                          | DS_034 Date of Birth                                                                                                                                                                                                                                                   | DS_034 Date of Birth                                                                                                                                                                                                                                                   |
| Component  Parts  | Age  Gender                                                                                                                                                                                                                                                            | DS_120 Age  DS_037 Gender                                                                                                                                                                                                                                              | DS_120 Age  DS_037 Gender                                                                                                                                                                                                                                              |
| Component  Parts  | 2. At least one of the following contact references must be included:                                                                                                                                                                                                  | 2. At least one of the following contact references must be included:                                                                                                                                                                                                  | 2. At least one of the following contact references must be included:                                                                                                                                                                                                  |
| Component  Parts  | Home Address                                                                                                                                                                                                                                                           | Home Address                                                                                                                                                                                                                                                           | This is the self-declared home address  This is an instance of  Address (DS_005, DS_007,  DS_008, DS_009, DS_010)                                                                                                                                                      |
| Component  Parts  | Telephone Number                                                                                                                                                                                                                                                       | Telephone Number                                                                                                                                                                                                                                                       | O_003 Telephone Number                                                                                                                                                                                                                                                 |
| Component  Parts  | Email Address                                                                                                                                                                                                                                                          | Email Address                                                                                                                                                                                                                                                          | O_004 Email Address                                                                                                                                                                                                                                                    |
| Validation  Rules | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                                                                                                                                                                                   | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                                                                                                                                                                                   | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                                                                                                                                                                                   |
| Validation  Rules | 2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number                                                                                                                                                                       | 2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number                                                                                                                                                                       | 2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number                                                                                                                                                                       |
| Validation  Rules | 3. Email Address  can repeat as a Person can have multiple occurrences of an  email address  4. See Component Standards for all components.                                                                                                                            | 3. Email Address  can repeat as a Person can have multiple occurrences of an  email address  4. See Component Standards for all components.                                                                                                                            | 3. Email Address  can repeat as a Person can have multiple occurrences of an  email address  4. See Component Standards for all components.                                                                                                                            |
| Related  Terms    |                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                        |

Notes

-  See General Validation Notes

## 2.13: Associations

| Ref No:   | P_013   | Entity   | Associations   | Associations    |
|-----------|---------|----------|----------------|-----------------|
| Class:    | Person  | Owner:   |                | Steward:        |
| Version:  |         | Status:  | Draft          | Approval  Date: |

## Minimum Completeness Requirement

| Description       | The 'Associations' entity is the collection of data components and validation  rules that describe an association as required by POLE. An Associate is related  to another person such as boyfriend, carer, colleague, business associate   | The 'Associations' entity is the collection of data components and validation  rules that describe an association as required by POLE. An Associate is related  to another person such as boyfriend, carer, colleague, business associate   | The 'Associations' entity is the collection of data components and validation  rules that describe an association as required by POLE. An Associate is related  to another person such as boyfriend, carer, colleague, business associate   |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                                                                                                                                                             | 1. The following component parts are mandatory:                                                                                                                                                                                             | 1. The following component parts are mandatory:                                                                                                                                                                                             |
| Component  Parts  | Given Name                                                                                                                                                                                                                                  | DS_031 Given Name                                                                                                                                                                                                                           | DS_031 Given Name                                                                                                                                                                                                                           |
| Component  Parts  | Surname                                                                                                                                                                                                                                     | DS_032 Surname                                                                                                                                                                                                                              | DS_032 Surname                                                                                                                                                                                                                              |
| Component  Parts  | Date of Birth                                                                                                                                                                                                                               | DS_034 Date of Birth                                                                                                                                                                                                                        | DS_034 Date of Birth                                                                                                                                                                                                                        |
| Component  Parts  | Age                                                                                                                                                                                                                                         | DS_120 Age                                                                                                                                                                                                                                  | DS_120 Age                                                                                                                                                                                                                                  |
| Component  Parts  | Gender                                                                                                                                                                                                                                      | DS_037 Gender                                                                                                                                                                                                                               | DS_037 Gender                                                                                                                                                                                                                               |
| Component  Parts  | 2. At least one of the following contact references must be included:                                                                                                                                                                       | 2. At least one of the following contact references must be included:                                                                                                                                                                       | 2. At least one of the following contact references must be included:                                                                                                                                                                       |
| Component  Parts  | Home Address                                                                                                                                                                                                                                | Home Address                                                                                                                                                                                                                                | This is the self-declared home address  This is an instance of  Address (DS_005, DS_007,  DS_008, DS_009, DS_010)                                                                                                                           |
| Component  Parts  | Telephone Number                                                                                                                                                                                                                            | Telephone Number                                                                                                                                                                                                                            | DS_053 Telephone Number                                                                                                                                                                                                                     |
| Component  Parts  | Email Address                                                                                                                                                                                                                               | Email Address                                                                                                                                                                                                                               |                                                                                                                                                                                                                                             |
| Component  Parts  | can repeat as a Person can have multiple occurrences of a                                                                                                                                                                                   | can repeat as a Person can have multiple occurrences of a                                                                                                                                                                                   | DS_054 Email Address                                                                                                                                                                                                                        |
| Validation  Rules | 1. Given Name  given name   2. Telephone Number of a telephone number                                                                                                                                                                       | 1. Given Name  given name   2. Telephone Number of a telephone number                                                                                                                                                                       | can repeat as a Person can have multiple occurrences                                                                                                                                                                                        |

[Image]

[Image]

|                | 4. See Component Standards for all components.   |
|----------------|--------------------------------------------------|
| Related  Terms |                                                  |
| Notes          |  See General Validation Notes                   |

Description

Component

Parts

[Image]

## 2.14: Missing Persons

| Ref No:   | P_014   | Entity   | Missing Persons   | Missing Persons   |
|-----------|---------|----------|-------------------|-------------------|
| Class:    | Person  | Owner:   |                   | Steward:          |
| Version:  |         | Status:  | Draft             | Approval  Date:   |

## Minimum Completeness Requirement

The national definition of a 'Missing Person' is 'anyone whose whereabouts cannot be established and where the circumstances are out of character or the context suggests the person may be subject of crime or risk of harm to themselves or another'. (NPCC/CoP)

Anyone whose whereabouts cannot be established will be considered as missing until located, and their well-being or otherwise confirmed.

All reports of missing people sit within a continuum of risk from 'no apparent risk (absent)' through to high-risk cases that require immediate, intensive action.

## Drawn from APP

1. The following component parts are mandatory:
2. At least one of the following contact references must be included:

Given Name

DS\_031 Given Name

Surname

DS\_032 Surname

Date of Birth

DS\_034 Date of Birth

Age

DS\_120 Age

Gender

DS\_037 Gender

Home Address

This is the self-declared home address This is an instance of Address (DS\_005, DS\_007,

DS\_008, DS\_009, DS\_010)

Telephone Number Email Address

DS\_053 Telephone Number DS\_054 Email Address

## Validation

Rules

## Related Terms

Notes

3. At least 4 of the following component parts must be included:
1. Given Name can repeat as a Person can have multiple occurrences of a given name
2. Telephone Number can repeat as a Person can have multiple occurrences of a telephone number
3. Email Address can repeat as a Person can have multiple occurrences of an email address
4. See Component Standards for all components.
6.  See General Validation Notes

Gender

DS\_037 Gender

Build

DS\_039 Build

Complexion

DS\_040 Complexion

Distinguishing Features

DS\_043 Distinguishing Features

Eye Colour - Left

DS\_041 Eye Colour Left

Eye Colour - Right

DS\_042 Eye Colour Right

Ethnicity

DS\_038 Ethnicity

Hair Colour

DS\_046 Hair Colour

[Image]

[Image]

## 2.15: Officer on Duty

| Ref No:   | P_015   | Entity   | Officer on Duty   | Officer on Duty   |
|-----------|---------|----------|-------------------|-------------------|
| Class:    | Person  | Owner:   |                   | Steward:          |
| Version:  |         | Status:  | Draft             | Approval  Date:   |

## Minimum Completeness Requirement

| Description       | The 'Officer on Duty' is the Officer logging details (using their unique collar  number)                                                                           |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                                                                                    |
| Validation  Rules | Collar Number  DS_070 Collar Number  1. If an officer is OFF duty another appropriate Person entity should be used  2. See Component Standards for all components. |
| Related  Terms    |                                                                                                                                                                    |
| Notes             |  See General Validation Notes                                                                                                                                     |

[Image]

## 2.16: Victim whilst on Duty

| Ref No:   | P_016   | Entity   | Victim whilst on Duty   | Victim whilst on Duty   |
|-----------|---------|----------|-------------------------|-------------------------|
| Class:    | Person  | Owner:   |                         | Steward:                |
| Version:  |         | Status:  | Draft                   | Approval  Date:         |

## Minimum Completeness Requirement

| Description       | A victim whilst on duty is a police officer who is subjected to an incident or  crime as a victim. The generic definition of a victim applies.                                | A victim whilst on duty is a police officer who is subjected to an incident or  crime as a victim. The generic definition of a victim applies.                                |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:  2.                                                                                                                           | At least one of the following contact references must be included:                                                                                                            |
|                   | Given Name  Surname  Date of Birth  Age  Gender                                                                                                                               | DS_031 Given Name  DS_032 Surname  DS_034 Date of Birth DS_120 Age  DS_037 Gender                                                                                             |
| Validation  Rules | 1. Given Name  given name   2. Telephone Number of a telephone number  3. Email Address email address  4. See Component Standards for all components.                         | 1. Given Name  given name   2. Telephone Number of a telephone number  3. Email Address email address  4. See Component Standards for all components.                         |
|                   | can repeat as a Person can have multiple occurrences of a   can repeat as a Person can have multiple occurrences   can repeat as a Person can have multiple occurrences of an | can repeat as a Person can have multiple occurrences of a   can repeat as a Person can have multiple occurrences   can repeat as a Person can have multiple occurrences of an |
| Related  Terms    |  Officer on Duty                                                                                                                                                             |  Officer on Duty                                                                                                                                                             |

## Notes

-  See General Validation Notes

## 2.17: Person Reporting / Organisation

| Ref No:   | P_017   | Entity   | Person Reporting / Organisation   | Person Reporting / Organisation   |
|-----------|---------|----------|-----------------------------------|-----------------------------------|
| Class:    | Person  | Owner:   |                                   | Steward:                          |
| Version:  |         | Status:  | Draft                             | Approval  Date:                   |

## Minimum Completeness Requirement

| Description       | The 'Person Reporting / Organisation' describes a person reporting an event on  behalf of an organisation.   | The 'Person Reporting / Organisation' describes a person reporting an event on  behalf of an organisation.   |
|-------------------|--------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                              | 1. The following component parts are mandatory:                                                              |
| Component  Parts  | Given Name  Surname                                                                                          | DS_031 Given Name  DS_032 Surname  DS_034 Date of Birth                                                      |
| Component  Parts  | Date of Birth                                                                                                |                                                                                                              |
| Component  Parts  | Age                                                                                                          | DS_120 Age                                                                                                   |
| Component  Parts  | Gender                                                                                                       | DS_037 Gender                                                                                                |
| Component  Parts  | 2. At least one of the following contact references must be included:                                        | 2. At least one of the following contact references must be included:                                        |
| Component  Parts  | Business Address                                                                                             | This is the self-declared business address                                                                   |
| Component  Parts  |                                                                                                              | This is an instance of  Address (DS_005, DS_007,                                                             |
| Component  Parts  | Telephone Number                                                                                             | DS_053 Telephone Number                                                                                      |
| Component  Parts  | Email Address                                                                                                | DS_054 Email Address                                                                                         |
| Validation  Rules | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                         | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                         |
| Validation  Rules | 2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number             | 2. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number             |
| Validation  Rules | email address  4. See Component Standards for all components.                                                | email address  4. See Component Standards for all components.                                                |

[Image]

[Image]

| Related  Terms   |  Person Reporting / General Public   |
|------------------|---------------------------------------|
| Notes            |  See General Validation Notes        |

## 2.18: Person Reporting / General Public

| Ref No:   | P_018   | Entity   | Person Reporting / General Public   | Person Reporting / General Public   |
|-----------|---------|----------|-------------------------------------|-------------------------------------|
| Class:    | Person  | Owner:   |                                     | Steward:                            |
| Version:  |         | Status:  | Draft                               | Approval  Date:                     |

## Minimum Completeness Requirement

| Description       | The 'Person Reporting / General Public' describes a person reporting an event  themselves                                                                        | The 'Person Reporting / General Public' describes a person reporting an event  themselves                                                                                                                                                                     |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:  Gender                                                                                                          | 1. The following component parts are mandatory:  Gender                                                                                                                                                                                                       |
|                   | Date of Birth  Age  2. Home Address  Telephone Number                                                                                                            | DS_034 Date of Birth DS_120 Age DS_037 Gender  At least one of the following contact references must be included:  This is the self-declared home address  This is an instance of  Address (DS_005, DS_007,  DS_008, DS_009, DS_010)  DS_053 Telephone Number |
| Validation  Rules | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name   2. Telephone Number  can repeat as a Person can have multiple occurrences | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name   2. Telephone Number  can repeat as a Person can have multiple occurrences                                                                                              |

[Image]

|                | 3. Email Address  can repeat as a Person can have multiple occurrences of an  email address  4. See Component Standards for all components.   |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Related  Terms |  Person Reporting / Organisation                                                                                                             |
| Notes          |  See General Validation Notes                                                                                                                |

## 2.19: Sudden Death / No Crime / Non-suspicious

| Ref No:   | P_019   | Entity   | Sudden Death / No Crime / Non-suspicious   | Sudden Death / No Crime / Non-suspicious   | Sudden Death / No Crime / Non-suspicious   |
|-----------|---------|----------|--------------------------------------------|--------------------------------------------|--------------------------------------------|
| Class:    | Person  | Owner:   |                                            | Steward:                                   |                                            |
| Version:  |         | Status:  | Draft                                      | Approval  Date:                            |                                            |

## Minimum Completeness Requirement

| Description      | When a death is not thought to be suspicious, it means nobody else was  involved .  This could mean the death was an accident, suicide or natural causes.   | When a death is not thought to be suspicious, it means nobody else was  involved .  This could mean the death was an accident, suicide or natural causes.                                                                  |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts | 1. The following component parts are mandatory:                                                                                                             | 1. The following component parts are mandatory:                                                                                                                                                                            |
| Component  Parts | Given Name  Surname  Date of Birth  Age  Gender                                                                                                             | DS_031 Given Name  DS_032 Surname  DS_034 Date of Birth DS_120 Age  This is the assumed gender  DS_037 Gender  This is the assumed home address  This is an instance of  Address (DS_005, DS_007,  DS_008, DS_009, DS_010) |
| Component  Parts | Date of Death                                                                                                                                               |                                                                                                                                                                                                                            |
| Component  Parts | Home Address                                                                                                                                                |                                                                                                                                                                                                                            |
| Component  Parts |                                                                                                                                                             | DS_076 Date of Death                                                                                                                                                                                                       |
| Component  Parts |                                                                                                                                                             |                                                                                                                                                                                                                            |

[Image]

|                   | Verification of Death  2.                                                                                                                                                                                                                                  | DS_075 Verification of Death                                                                                                                                                                                                                               |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                   | At least one of the following contact references must be included:                                                                                                                                                                                         | At least one of the following contact references must be included:                                                                                                                                                                                         |
|                   | Telephone Number                                                                                                                                                                                                                                           | DS_053 Telephone Number                                                                                                                                                                                                                                    |
|                   | Email Address                                                                                                                                                                                                                                              | DS_054 Email Address                                                                                                                                                                                                                                       |
| Validation  Rules | 1. Date of Death  must not be earlier than person's date of birth  2. Given Name  can repeat as a Person can have multiple occurrences of a  given name   3. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number | 1. Date of Death  must not be earlier than person's date of birth  2. Given Name  can repeat as a Person can have multiple occurrences of a  given name   3. Telephone Number  can repeat as a Person can have multiple occurrences  of a telephone number |
| Related  Terms    |                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                            |
|                   | 4.                                                                                                                                                                                                                                                         | Email Address  can repeat as a Person can have multiple occurrences of an  email address                                                                                                                                                                   |
|                   | 5.                                                                                                                                                                                                                                                         | See Component Standards for all components.                                                                                                                                                                                                                |
| Notes             |  See General Validation Notes                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                            |

[Image]

## 2.20: Sudden Death / Victim / Unexplained

| Ref No:   | P_020   | Entity   | Sudden Death / Victim / Unexplained   | Sudden Death / Victim / Unexplained   | Sudden Death / Victim / Unexplained   |
|-----------|---------|----------|---------------------------------------|---------------------------------------|---------------------------------------|
| Class:    | Person  | Owner:   |                                       | Steward:                              |                                       |
| Version:  |         | Status:  | Draft                                 | Approval  Date:                       |                                       |

## Minimum Completeness Requirement

| Description                                                                                                                                                                                          | Sudden death of an infant or child or sudden death where the age of the  deceased is under 30 years of age, a death resulting from a previous accident /  trauma or persons found dead after forced entry into premises.   Those in attendance believe that the circumstances are such that a further  detailed investigation should take place to establish if any suspicious  circumstances exist.   | Sudden death of an infant or child or sudden death where the age of the  deceased is under 30 years of age, a death resulting from a previous accident /  trauma or persons found dead after forced entry into premises.   Those in attendance believe that the circumstances are such that a further  detailed investigation should take place to establish if any suspicious  circumstances exist.   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  1. Given Name  Surname  Date of Birth  Age  Gender  Home Address  DS_008, DS_009, DS_010)  Date of Death  DS_076 Date of Death Verification of Death  DS_075 Verification of Death | The following component parts are mandatory:                                                                                                                                                                                                                                                                                                                                                           | The following component parts are mandatory:                                                                                                                                                                                                                                                                                                                                                           |
|                                                                                                                                                                                                      | DS_031 Given Name  DS_032 Surname  DS_034 Date of Birth DS_120 Age                                                                                                                                                                                                                                                                                                                                     | This is the assumed gender  DS_037 Gender  This is the self-declared home address  This is an instance of  Address (DS_005, DS_007,                                                                                                                                                                                                                                                                    |
| 2. Telephone Number  DS_053 Telephone Number                                                                                                                                                         | At least one of the following contact references must be included:  Email Address  DS_054 Email Address                                                                                                                                                                                                                                                                                                | At least one of the following contact references must be included:  Email Address  DS_054 Email Address                                                                                                                                                                                                                                                                                                |

[Image]

|                | 4. See Component Standards for all components.   |
|----------------|--------------------------------------------------|
| Related  Terms |                                                  |
| Notes          |  See General Validation Notes                   |

## 3. Minimum Data Standards for OBJECT Entities

## 3.1: Vehicle Known

| Ref No:   | O_001   | Entity   | Vehicle Known   | Vehicle Known   |
|-----------|---------|----------|-----------------|-----------------|
| Class:    | Object  | Owner:   |                 | Steward:        |
| Version:  |         | Status:  | Draft           | Approval  Date: |

## Minimum Completeness Requirement

| Description       | A known vehicle is a vehicle where a full description can be given of  manufacturer, model, type, colour and importantly VRM. The make and model  should use DfT/DVLA data set that is currently used by PND.   | A known vehicle is a vehicle where a full description can be given of  manufacturer, model, type, colour and importantly VRM. The make and model  should use DfT/DVLA data set that is currently used by PND.   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:  Vehicle Registration Mark  Vehicle Make  Vehicle Model  Vehicle Body Shape  Vehicle Colour  DS_069 Vehicle Colour                                              | DS_065 VRM  DS_066 Vehicle Make  DS_067 Vehicle Model  DS_068 Vehicle Shape                                                                                                                                     |
| Validation  Rules | 1. There may be multiple vehicle colours  2. See Component Standards for all components.                                                                                                                        | 1. There may be multiple vehicle colours  2. See Component Standards for all components.                                                                                                                        |
| Related  Terms    |  Vehicle - Suspicious                                                                                                                                                                                          |  Vehicle - Suspicious                                                                                                                                                                                          |
| Notes             |  See General Validation Notes                                                                                                                                                                                  |                                                                                                                                                                                                                 |

[Image]

[Image]

## 3.2: Vehicle Suspicious

| Ref No:   | O_002   | Entity   | Vehicle Suspicious   | Vehicle Suspicious   |
|-----------|---------|----------|----------------------|----------------------|
| Class:    | Object  | Owner:   |                      | Steward:             |
| Version:  |         | Status:  | Draft                | Approval  Date:      |

## Minimum Completeness Requirement

| Description       | A suspicious vehicle is a vehicle which is or has acted in a suspicious manner  and requires further investigation. Details could be partial or known.  Minimum standards for a 'suspicious vehicle' are difficult to put in place,  suggest none at first draft.   | A suspicious vehicle is a vehicle which is or has acted in a suspicious manner  and requires further investigation. Details could be partial or known.  Minimum standards for a 'suspicious vehicle' are difficult to put in place,  suggest none at first draft.   |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. At least one of the following component parts must be completed (to the  extend described)  Vehicle Registration Mark  (partial or full) Vehicle Make  (if known) Vehicle Model  (if known) Vehicle Body Shape  (if known) Vehicle Colour                        | DS_065 VRM   DS_066 Vehicle Make   DS_067 Vehicle Model   DS_068 Vehicle Shape  (if known)  DS_069 Vehicle Colour                                                                                                                                                   |
| Validation  Rules | 1. There may be multiple vehicle colours  2. See Component Standards for all components.                                                                                                                                                                            | 1. There may be multiple vehicle colours  2. See Component Standards for all components.                                                                                                                                                                            |
| Related  Terms    |  Vehicle - Known                                                                                                                                                                                                                                                   |  Vehicle - Known                                                                                                                                                                                                                                                   |
| Notes             |  See General Validation Notes                                                                                                                                                                                                                                      |  See General Validation Notes                                                                                                                                                                                                                                      |

[Image]

## 3.3: Telephone

| Ref No:   | O_003   | Entity   | Telephone   |                 |
|-----------|---------|----------|-------------|-----------------|
| Class:    | Object  | Owner:   |             | Steward:        |
| Version:  |         | Status:  | Draft       | Approval  Date: |

## Minimum Completeness Requirement

| Description       | A telephone in this context is the full telephone number, including the type of  number (such as landline), country code (such as UK) and the full STD number  (eg +441234567890) with, if needed the addition of an extension number.   | A telephone in this context is the full telephone number, including the type of  number (such as landline), country code (such as UK) and the full STD number  (eg +441234567890) with, if needed the addition of an extension number.   |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                                                                                                                                                          | 1. The following component parts are mandatory:                                                                                                                                                                                          |
|                   | Telephone Number Type  Full Telephone Number  Telephone Country                                                                                                                                                                          | DS_051 Telephone Type Code  This is the full telephone number with  international dialling code  DS_053 Telephone Number  DS_052 Telephone Country                                                                                       |
| Validation  Rules | 1. See Component Standards for all components.                                                                                                                                                                                           | 1. See Component Standards for all components.                                                                                                                                                                                           |
| Related  Terms    |                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                          |
| Notes             |  See General Validation Notes                                                                                                                                                                                                           |  See General Validation Notes                                                                                                                                                                                                           |

[Image]

## 3.4: Email

| Ref No:   | O_004   | Entity   | Email   |                 |
|-----------|---------|----------|---------|-----------------|
| Class:    | Object  | Owner:   |         | Steward:        |
| Version:  |         | Status:  | Draft   | Approval  Date: |

## Minimum Completeness Requirement

| Description       | The email address is the virtual address for a person, or persons, or  organisation. As an entity it can be used multiple times and be related to  multiple people / organisations.   |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component part is mandatory:  Email Address  DS_054 Email Address                                                                                                    |
| Validation  Rules | 1. See Component Standard for component definition.                                                                                                                                   |
| Related  Terms    |                                                                                                                                                                                       |
| Notes             |  See General Validation Notes                                                                                                                                                        |

[Image]

## 3.5: Passport

| Ref No:   | O_005   | Entity   | Passport   |                 |
|-----------|---------|----------|------------|-----------------|
| Class:    | Object  | Owner:   | HMPO       | Steward:        |
| Version:  |         | Status:  | Draft      | Approval  Date: |

## Minimum Completeness Requirement

| Description       | The passport in this case is the identifying characteristics of the passport that  identify a person. Included is the requirement to describe whether the passport  is valid and whether it is UK or foreign.   | The passport in this case is the identifying characteristics of the passport that  identify a person. Included is the requirement to describe whether the passport  is valid and whether it is UK or foreign.   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component part is mandatory:                                                                                                                                                                   | DS_056 UK Passport Number                                                                                                                                                                                       |
|                   | Passport Validity  Passport Country  2. If the passport is UK the following component part is mandatory:  UK Passport Number                                                                                    | DS_058 Passport Validity  DS_059 Passport Country                                                                                                                                                               |
| Validation  Rules | Foreign Passport Number  DS_057 Foreign Passport Number  1. See Component Standards for all components.  2. This can only be recorded as accurate is documentation is present                                   | Foreign Passport Number  DS_057 Foreign Passport Number  1. See Component Standards for all components.  2. This can only be recorded as accurate is documentation is present                                   |
| Related  Terms    |                                                                                                                                                                                                                 |                                                                                                                                                                                                                 |
| Notes             |  See General Validation Notes                                                                                                                                                                                  |  See General Validation Notes                                                                                                                                                                                  |

[Image]

## 3.6: Driving Licence

| Ref No:   | O_006   | Entity   | Driving Licence   | Driving Licence   | Driving Licence   |
|-----------|---------|----------|-------------------|-------------------|-------------------|
| Class:    | Object  | Owner:   | DVLA              | Steward:          | DVLA              |
| Version:  |         | Status:  | Draft             | Approval  Date:   |                   |

| Minimum Completeness Requirement   | Minimum Completeness Requirement                                                                                                                                                                                                                                                                                                                                                         | Minimum Completeness Requirement                                                                                                                                                                                                                                                                                                                                                         |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description                        | A driving licence can be UK or foreign and can be used as a form of identity  associated with a person.                                                                                                                                                                                                                                                                                  | A driving licence can be UK or foreign and can be used as a form of identity  associated with a person.                                                                                                                                                                                                                                                                                  |
| Component  Parts                   | 1. If the Driving Licence is UK the following component part is mandatory:                                                                                                                                                                                                                                                                                                               | 1. If the Driving Licence is UK the following component part is mandatory:                                                                                                                                                                                                                                                                                                               |
|                                    | UK Driving Licence Number  DS_061 UK Driving Licence Number  2. If the Driving Licence is foreign the following component parts are  mandatory:  Foreign Driving Licence Number  DS_062 Foreign Driving Licence  Number  Driving Licence Country  DS_063 Driving Licence Country                                                                                                         |                                                                                                                                                                                                                                                                                                                                                                                          |
| Validation  Rules                  | 1. If the 'Driving Licence' entity is UK the following components should not be  completed:   Foreign Driving Licence Number   Country Code   (this is defaulted as GBR and no editing is required)  2. If the 'Driving Licence' entity is foreign the following data component  should not be completed:   UK Driving Licence Number  3. See Component Standards for all components. | 1. If the 'Driving Licence' entity is UK the following components should not be  completed:   Foreign Driving Licence Number   Country Code   (this is defaulted as GBR and no editing is required)  2. If the 'Driving Licence' entity is foreign the following data component  should not be completed:   UK Driving Licence Number  3. See Component Standards for all components. |
| Related  Terms                     |                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                          |
| Notes                              |  See General Validation Notes                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                          |

[Image]

## 3.7: CRO Number

| Ref No:   | O_007   | Entity   | CRO Number (Criminal Records Office  number)   | CRO Number (Criminal Records Office  number)   |
|-----------|---------|----------|------------------------------------------------|------------------------------------------------|
| Class:    | Object  | Owner:   |                                                | Steward:                                       |
| Version:  |         | Status:  | Draft                                          | Approval  Date:                                |

| Minimum Completeness Requirement   | Minimum Completeness Requirement                                                                                                                                                                                      |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description                        | The CRO is assigned to a person the first time they are charged with or  summonsed for an offence and can be used as an identifier for the person. CRO  is issued upon biometric confirmation of a new person record. |
| Component  Parts                   | 1. The following component part is mandatory:  CRO Number  DS_071 Criminal Records Office Number                                                                                                                      |
| Validation  Rules                  | 1. See Component Standards for all components.                                                                                                                                                                        |
| Related  Terms                     |                                                                                                                                                                                                                       |
| Notes                              |  See General Notes                                                                                                                                                                                                   |

[Image]

## 3.8: PNC ID

| Ref No:   | O_008   | Entity   | PNC ID   |                 |
|-----------|---------|----------|----------|-----------------|
| Class:    | Object  | Owner:   |          | Steward:        |
| Version:  |         | Status:  | Draft    | Approval  Date: |

## Minimum Completeness Requirement

Description

Each record on the PNC is allocated a unique system generated reference when it is first created on the system, which may be used to retrieve a record. This is called the PNC ID and it consists of a two digit year element (relative to the year in which the record originated), up to a seven digit serial number (leading zeros are omitted), followed by one computer generated check letter, e.g. 90/570L.

Each Person record on the PNC, including those not involved in criminality such as licensed firearm certificate holders and Missing Persons is allocated a unique system generated reference when it is first created on the system.

## Component Parts

1. The following component part is mandatory:

PNC ID

DS\_072 Police National Computer ID

Validation

Rules

1. See Component Standards for all components.

## Related Terms

Notes

-  See General Validation Notes

[Image]

## 3.9: NI Number

| Ref No:   | O_009   | Entity   | NI Number   | NI Number       | NI Number   |
|-----------|---------|----------|-------------|-----------------|-------------|
| Class:    | Object  | Owner:   | DWP         | Steward:        | DWP         |
| Version:  |         | Status:  | Draft       | Approval  Date: |             |

## Minimum Completeness Requirement

| Description       | A national insurance number is a unique identifier for a person that is used to  make sure your National Insurance contributions and tax are recorded against  your name only. NI Numbers are issued by the Department for Work and  Pensions.   |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component part is mandatory:  NI Number  DS_060 National Insurance Number                                                                                                                                                       |
| Validation  Rules | 1. See Component Standards for all components.                                                                                                                                                                                                   |
| Related  Terms    |                                                                                                                                                                                                                                                  |
| Notes             |  See General Validation Notes                                                                                                                                                                                                                   |

[Image]

## 3.10: Property

| Ref No:   | O_010   | Entity   | Property   | Property        | Property   |
|-----------|---------|----------|------------|-----------------|------------|
| Class:    | Object  | Owner:   |            | Steward:        |            |
| Version:  |         | Status:  | Draft      | Approval  Date: |            |

## Minimum Completeness Requirement

| Description       | Property includes all objects, things in action and other tangible or intangible  items, excluding vehicles, land or buildings which are created as individual POLE  entities.  It could be a mobile phone in which case there would be an IMEI or bicycle that  may have a security code etched. When available, identifying numbers should  be used to provide uniqueness to the property.                                                                            | Property includes all objects, things in action and other tangible or intangible  items, excluding vehicles, land or buildings which are created as individual POLE  entities.  It could be a mobile phone in which case there would be an IMEI or bicycle that  may have a security code etched. When available, identifying numbers should  be used to provide uniqueness to the property.                                                                            |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                                                                                                                                                                                                                                                                                                                                                                                         | 1. The following component parts are mandatory:                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Component  Parts  | Category  Property Description                                                                                                                                                                                                                                                                                                                                                                                                                                          | DS_097 Property - Category  DS_098 Property - Description                                                                                                                                                                                                                                                                                                                                                                                                               |
| Component  Parts  | 2. If the property has some form of identity code the following component  parts are mandatory:                                                                                                                                                                                                                                                                                                                                                                         | 2. If the property has some form of identity code the following component  parts are mandatory:                                                                                                                                                                                                                                                                                                                                                                         |
| Component  Parts  | Unique ID Type  Unique ID                                                                                                                                                                                                                                                                                                                                                                                                                                               | DS_099 Unique ID Number Type  DS_100 Unique Number                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Validation  Rules | 1. Property Description should include where possible:   Characteristic Material   Period   Shape   Primary Colour   Secondary Colour   Role in the incident  2. The 'Unique ID Number Type' must match to 'Property Category'  e.g. If property category is 'Mobile Phone' then unique ID number type  must align - so IMEI or IMSI or SIM  3. Multiple instances of ID Number Type and Unique Numbers can be used.  e.g. a mobile phone may have SIM  and  IMEI | 1. Property Description should include where possible:   Characteristic Material   Period   Shape   Primary Colour   Secondary Colour   Role in the incident  2. The 'Unique ID Number Type' must match to 'Property Category'  e.g. If property category is 'Mobile Phone' then unique ID number type  must align - so IMEI or IMSI or SIM  3. Multiple instances of ID Number Type and Unique Numbers can be used.  e.g. a mobile phone may have SIM  and  IMEI |

[Image]

| Related  Terms   |                                |
|------------------|--------------------------------|
| Notes            |  See General Validation Notes |

## 3.11: Custody Image

| Ref No:   | O_011   | Entity   | Custody Image   | Custody Image   |
|-----------|---------|----------|-----------------|-----------------|
| Class:    | Object  | Owner:   |                 | Steward:        |
| Version:  |         | Status:  | Draft           | Approval  Date: |

## Minimum Completeness Requirement

| Description       | A term for facial photographs taken by police of individuals detained following  arrest but may also be obtained where a person is not arrested but reported  for a relevant offence. These are generally retained as police information for  identity reference, search and investigation.   | A term for facial photographs taken by police of individuals detained following  arrest but may also be obtained where a person is not arrested but reported  for a relevant offence. These are generally retained as police information for  identity reference, search and investigation.   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component         | 1. The following component parts are mandatory:                                                                                                                                                                                                                                               | 1. The following component parts are mandatory:                                                                                                                                                                                                                                               |
| Component         | Given Name                                                                                                                                                                                                                                                                                    | DS_031 Given Name                                                                                                                                                                                                                                                                             |
| Component         | Surname                                                                                                                                                                                                                                                                                       | DS_032 Surname                                                                                                                                                                                                                                                                                |
| Component         | Date of Birth                                                                                                                                                                                                                                                                                 | DS_034 Date of Birth                                                                                                                                                                                                                                                                          |
| Component         | Age                                                                                                                                                                                                                                                                                           | DS_120 Age                                                                                                                                                                                                                                                                                    |
| Component         | Custody Photograph                                                                                                                                                                                                                                                                            | DS_102 Photograph                                                                                                                                                                                                                                                                             |
| Parts             | 2. At least one of the following references must be included:                                                                                                                                                                                                                                 | 2. At least one of the following references must be included:                                                                                                                                                                                                                                 |
| Parts             | Offence                                                                                                                                                                                                                                                                                       | DS_080 Offence Type (Offence Code)                                                                                                                                                                                                                                                            |
| Parts             | Reason for Arrest  and                                                                                                                                                                                                                                                                        | DS_086 Arrest Reason                                                                                                                                                                                                                                                                          |
| Parts             | Arrest Summons Number                                                                                                                                                                                                                                                                         | DS_073 Arrest Summons Number                                                                                                                                                                                                                                                                  |
| Parts             | 3.                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                               |
| Parts             | Date of image taken                                                                                                                                                                                                                                                                           | This is an instance of  DS_001 Generic Date                                                                                                                                                                                                                                                   |
| Parts             | Time of image taken                                                                                                                                                                                                                                                                           | This is an instance of  DS_002 Generic Time                                                                                                                                                                                                                                                   |
| Validation  Rules | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                                                                                                                                                                                                          | 1. Given Name  can repeat as a Person can have multiple occurrences of a  given name                                                                                                                                                                                                          |

[Image]

|                | 2. If applicable, multiple instances of arrest  DS_086 Arrest Reason  should be  listed  3. See Component Standards for all components.                                                                                                                                                                     |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Related  Terms |                                                                                                                                                                                                                                                                                                             |
| Notes          |  See General Validation Notes   The Home Office published a review on their use and retention in 2017.  This followed concerns over the retention of the images of unconvicted  individuals, individuals who were under 18 when images were taken  and the length of time for which images were retained. |

## 3.12: Photograph

| Ref No:   | O_012   | Entity   | Photograph   | Photograph      |
|-----------|---------|----------|--------------|-----------------|
| Class:    | Object  | Owner:   |              | Steward:        |
| Version:  |         | Status:  | Draft        | Approval  Date: |

## Minimum Completeness Requirement

| Description       | An image captured on a photo-sensitive surface, usually a photographic film or  an electronic image sensor.   | An image captured on a photo-sensitive surface, usually a photographic film or  an electronic image sensor.   |
|-------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                               | 1. The following component parts are mandatory:                                                               |
|                   | Date of Photograph  Photograph Description                                                                    | DS_103 Date of Photograph DS_101 Photograph Description                                                       |
| Validation  Rules | 1. Date of Photograph  must not be in the future  2. See Component Standards for all components.              | 1. Date of Photograph  must not be in the future  2. See Component Standards for all components.              |
| Related  Terms    |                                                                                                               |                                                                                                               |
| Notes             |  See General Validation Notes                                                                                |                                                                                                               |

[Image]

## 3.13: Unique Social Media Tag

| Ref No:   | O_013   | Entity   | Unique Social Media Tag   | Unique Social Media Tag   |
|-----------|---------|----------|---------------------------|---------------------------|
| Class:    | Object  | Owner:   |                           | Steward:                  |
| Version:  |         | Status:  | Draft                     | Approval  Date:           |

| Minimum Completeness Requirement   | Minimum Completeness Requirement                                                         |
|------------------------------------|------------------------------------------------------------------------------------------|
| Description                        | A unique 'social media tag' identifies people, groups or things in a post or  photo.     |
| Component  Parts                   | 1. The following component part is mandatory:  Social Media Tag  DS_055 Social Media Tag |
| Validation  Rules                  | 1. See Component Standards for all components.                                           |
| Related  Terms                     |                                                                                          |
| Notes                              |  See General Notes                                                                      |

## 4. Minimum Data Standards for LOCATION Entities

## 4.1: Residential Address

| Ref No:   | L_001    | Entity   | Residential Address   | Residential Address   |
|-----------|----------|----------|-----------------------|-----------------------|
| Class:    | Location | Owner:   |                       | Steward:              |
| Version:  |          | Status:  | Draft                 | Approval  Date:       |

| Minimum Completeness Requirement                                            |                                                                                                 |
|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Description                                                                 | A residential address as opposed to a business address is one where persons  habitually reside. |
| 1. The following component parts are mandatory:  Postcode  DS_010 Postcode  |                                                                                                 |
| Street                                                                      |                                                                                                 |
| 3. As many as possible of the following component parts should be included: |                                                                                                 |
|                                                                             | DS_007 Street                                                                                   |
| Town                                                                        | DS_008 Town                                                                                     |
| County                                                                      | DS_009 County                                                                                   |
| Country Code                                                                | DS_004 Country                                                                                  |
| Property UPRN                                                               | DS_011 Property UPRN                                                                            |
| 1. See Component Standards for all components.                              |                                                                                                 |
| Validation                                                                  |                                                                                                 |
| Rules                                                                       |                                                                                                 |
| Related                                                                     |                                                                                                 |
| Terms                                                                       |                                                                                                 |

[Image]

## Notes

-  See General Validation Notes

[Image]

[Image]

## 4.2: Business Address

| Ref No:   | L_002    | Entity   | Business Address   | Business Address   |
|-----------|----------|----------|--------------------|--------------------|
| Class:    | Location | Owner:   |                    | Steward:           |
| Version:  |          | Status:  | Draft              | Approval  Date:    |

| Minimum Completeness Requirement   | Minimum Completeness Requirement                                                                    | Minimum Completeness Requirement                                                                    |
|------------------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Description                        | A business address as opposed to a residential address is one where a  registered business resides. | A business address as opposed to a residential address is one where a  registered business resides. |
| Component  Parts                   | 1. The following component parts are mandatory:  2. Unit Number                                     | As many as possible of the following component parts should be included:  DS_013 Unit Number        |
|                                    | Business Name  Premises Name or Number  Postcode                                                    | DS_012 Business Name  DS_006 Premises  DS_010 Postcode                                              |
| Validation  Rules                  | 1. See Component Standards for all components.                                                      | 1. See Component Standards for all components.                                                      |
| Related  Terms                     |                                                                                                     |                                                                                                     |
| Notes                              |  See General Validation Notes                                                                      |                                                                                                     |

[Image]

## 4.3: Location - Geometric

| Ref No:   | L_003    | Entity   | Location - Geometric   | Location - Geometric   |
|-----------|----------|----------|------------------------|------------------------|
| Class:    | Location | Owner:   |                        | Steward:               |
| Version:  |          | Status:  | Draft                  | Approval  Date:        |

## Minimum Completeness Requirement

| Description       | A Geometric location is denoted by grid references or latitude and longitude.  Latitude and Longitude can be used to provide a location globally.   | A Geometric location is denoted by grid references or latitude and longitude.  Latitude and Longitude can be used to provide a location globally.   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:                                                                                                     | 1. The following component parts are mandatory:                                                                                                     |
|                   | National GR - Latitude  National GR - Longitude                                                                                                     | DS_014 Latitude  DS_015 Longitude                                                                                                                   |
| Validation  Rules | 1. See Component Standards for all components.                                                                                                      | 1. See Component Standards for all components.                                                                                                      |
| Related  Terms    |                                                                                                                                                     |                                                                                                                                                     |
| Notes             |  See General Validation Notes                                                                                                                      |  See General Validation Notes                                                                                                                      |

[Image]

## 4.4: Location - Area

| Ref No:   | L_004    | Entity   | Location - Area   | Location - Area   |
|-----------|----------|----------|-------------------|-------------------|
| Class:    | Location | Owner:   |                   | Steward:          |
| Version:  |          | Status:  | Draft             | Approval  Date:   |

| Minimum Completeness Requirement   | Minimum Completeness Requirement                                                                                                                                                                                                                                                                                                                                                                    |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description                        | 'Location - Area' can be used when there is no other useful mechanism for  denoting location, where possible it is useful to use another location entity as a  reference (e.g. the NE corner of the field 100m west of GU10 0SD). If using  reference points these should be enduring in nature (ie a car is not a good  reference point once it is driven away, trees and bushes can be cut down). |
| Component  Parts                   | 1. The following component part is mandatory:  Location Description  DS_016 Location - Area                                                                                                                                                                                                                                                                                                         |
| Validation  Rules                  | 1. See Component Standards for all components.                                                                                                                                                                                                                                                                                                                                                      |
| Related  Terms                     |                                                                                                                                                                                                                                                                                                                                                                                                     |
| Notes                              |  See General Validation Notes                                                                                                                                                                                                                                                                                                                                                                      |

[Image]

## 4.5: Location - NFA

| Ref No:   | L_005    | Entity   | Location - NFA   | Location - NFA   |
|-----------|----------|----------|------------------|------------------|
| Class:    | Location | Owner:   |                  | Steward:         |
| Version:  |          | Status:  | Draft            | Approval  Date:  |

## Minimum Completeness Requirement

| Description       | 'Location - NFA' can be used when the person related to the event has no fixed  abode.   | 'Location - NFA' can be used when the person related to the event has no fixed  abode.                                              |
|-------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component part is mandatory:                                            | 1. The following component part is mandatory:                                                                                       |
|                   | Location - NFA                                                                           | This can be a description of the 'residential address'  or simply 'No Fixed Abode'.  This is an instance of  DS_016 Location - Area |
| Validation  Rules | 1. See Component Standards for all components.                                           | 1. See Component Standards for all components.                                                                                      |
| Related  Terms    |                                                                                          |                                                                                                                                     |
| Notes             |  See General Validation Notes                                                           |                                                                                                                                     |

## 5. Minimum Data Standards for EVENT Entities

## 5.1: Crime

| Ref No:   | E_001   |         | Crime   | Entity          |
|-----------|---------|---------|---------|-----------------|
| Class:    | Event   | Owner:  |         | Steward:        |
| Version:  |         | Status: | Draft   | Approval  Date: |

## Minimum Completeness Requirement

| Description      | A crime is a deliberate act that causes physical or psychological harm, damage  to or loss of property and is against the law.  Source: https://www.police.uk/pu/contact-the-police/what-and-how-to- report/what-report/   | A crime is a deliberate act that causes physical or psychological harm, damage  to or loss of property and is against the law.  Source: https://www.police.uk/pu/contact-the-police/what-and-how-to- report/what-report/                                                                                                                                                                                                                                                                                                                                                      |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts | 1. The following component parts are mandatory:  Home Office Classification  Crime Type  Resolved Outcome  Crime Status  Hate Crime?  Date of Offence  Time of Offence  MO  Reported Date                                  | DS_074 Home Office Classification  DS_078 Crime Type  DS_083 Crime Outcome  DS_084 Crime Status / Clear Up Method  DS_096 Hate Crime  This is the date that the offence occurs.  A crime can occur between two dates  specified, option of 'between' date  intervals can exist  This is an instance of  DS_001 Generic Date  This is the time that the offence occurred.  A crime can occur between two times  specified, option of 'between' time  intervals can exist  This is an instance of  DS_002 Generic Time DS_088 MO  This is the date that the offence is reported |

[Image]

## This is an instance of DS\_001 Generic Date

## Recording / Reporting Officer / Staff

A Recording / Reporting Officer/Staff is the individual who initially reports the details of a crime or incident.

This is an instance of DS\_070 Collar

## Number

## Supervising Officer

This is the line manager responsible for supervision of officers and staff involved in an incident, investigation or other police activity.

This is an instance of DS\_070 Collar

Number

2. At least one of the following location component parts must be included:

Location - Post Code

## DS\_010 Postcode

Location - Geometric

This is the Lat/Long Grid Reference for the Crime

This is an instance of DS\_015 Location - Longitude, DS\_014 Latitude

Location - Area

This is a description of where the crime took place.

This is an instance of DS\_016 Location - Area

3. If the 'resolved crime' is concluded then the following component part is mandatory:

Offender (if resolved crime) P\_001 Offender

4. If 'Hate Crime' is 'Yes' then the following component part is mandatory:

Correct Checks

## DS\_110 Correct Checks

## Validation Rules

1. Date of Offence must not be in the future

2. Time of Offence must not be in the future

3. MO must be at least 20 characters

4. See Component Standards for all components.

## Related Terms

-  Incident

-  Offender

[Image]

## Notes

-  See General Validation Notes

[Image]

[Image]

## 5.2: Incident

| Ref No:   | E_002   | Entity   | Incident   | Incident        |
|-----------|---------|----------|------------|-----------------|
| Class:    | Event   | Owner:   |            | Steward:        |
| Version:  |         | Status:  | Draft      | Approval  Date: |

## Minimum Completeness Requirement

| Description      | An event or situation with a range of consequences which requires  arrangements to be implemented by one or more emergency responder  agency .  An incident is a possible crime, an event that one is not sure yet whether a                                                                                                                                                                                                                                                                                                       | An event or situation with a range of consequences which requires  arrangements to be implemented by one or more emergency responder  agency .  An incident is a possible crime, an event that one is not sure yet whether a   |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts | crime has been committed.  1. The following component parts are mandatory:  Incident Qualifiers  DS_074 Home Office Classification  NSIR - Opening Code  DS_091 NSIR Opening Code NSIR - Closing Code  DS_092 NSIR Closing Code Person Information  P_008 Subject (Not Offender, Victim or  Witness)  Date of Incident  This is the date that the incident  occurred.  This is an instance of  DS_001 Generic  Date  Time of Incident  This is the time that the incident  occurred.  This is an instance of  DS_002 Generic  Time |                                                                                                                                                                                                                                |
| Component  Parts | 2. At least one of the following location component parts must be  included:                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 2. At least one of the following location component parts must be  included:                                                                                                                                                   |
| Component  Parts | Incident Location - Address                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Address (DS_005, DS_007, DS_008,  DS_009, DS_010)                                                                                                                                                                              |

[Image]

|                   | Incident Location - Geometric  Incident Location - Area                                                                               | This is the Lat/Long Grid Reference for  the Crime  This is an instance of  DS_015 Location -  Longitude, DS_014 Latitude This is a description of where the crime  took place.  This is an instance of  L_004 Location -  Area   |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation  Rules | Date of Incident  must not be in the future  Time of Incident  must not be in the future  See Component Standards for all components. |                                                                                                                                                                                                                                   |
| Related  Terms    |                                                                                                                                       |                                                                                                                                                                                                                                   |
| Notes             |  See General Validation Notes                                                                                                        |                                                                                                                                                                                                                                   |

[Image]

## 5.3: Custody

| Ref No:   | E_003   | Entity   | Custody   | Custody         |
|-----------|---------|----------|-----------|-----------------|
| Class:    | Event   | Owner:   |           | Steward:        |
| Version:  |         | Status:  | Draft     | Approval  Date: |

## Minimum Completeness Requirement

| Description       | Procedures that happen when someone is arrested and detained safely in  custody until disposal.                                                                                                                                | Procedures that happen when someone is arrested and detained safely in  custody until disposal.                                                                                                                                                                                                                                                                                                                                                  |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component  Parts  | 1. The following component parts are mandatory:  Custody Person Information  Arrest Summons Number  Offence Code  Reason for Arrest  Gender  Nationality  Self-defined Ethnicity  Officer defined Ethnicity  Arresting Officer | P_002 Suspect - Known  DS_073 Arrest Summons Number  DS_080 Offence Type (Offence Code)  DS_086 Arrest Reason  DS_037 Gender  This is the ethnicity as defined by the  individual being brought into custody  This is an instance of  DS_038 Ethnicity  This is the ethnicity as defined by the  arresting officer  DS_112 Officer Defined Ethnicity  This is the officer arresting the individual  This is an instance of  P_070 Collar  Number |
| Validation  Rules | 1. See Component Standards for all components.                                                                                                                                                                                 | 1. See Component Standards for all components.                                                                                                                                                                                                                                                                                                                                                                                                   |

[Image]

| Related  Terms   |                                |
|------------------|--------------------------------|
| Notes            |  See General Validation Notes |

[Image]

## 5.4: Stop Search

| Ref No:   | E_004   | Entity   | Stop Search   |                 |
|-----------|---------|----------|---------------|-----------------|
| Class:    | Event   | Owner:   |               | Steward:        |
| Version:  |         | Status:  | Draft         | Approval  Date: |

## Minimum Completeness Requirement

Description

The police have a range of statutory powers of stop and search available to them, depending on the circumstances. Most, but not all, of these powers require an officer to have reasonable grounds for suspicion that an unlawful item is being carried or a lawful item/s that may be used with criminal intent. The one thing the powers all have in common is that they allow officers to detain a person who is not under arrest in order to search them or their vehicle.

## Drawn from College of Policing

## Component Parts

1. The following component parts are mandatory:

Nature of Stop

Stop &amp; Search receipt

DS\_105 Stop Nature Reference Number DS\_031 Given Name DS\_032 Surname DS\_034 Date of Birth DS\_120 Age DS\_035 Place of Birth This is date of the stop and search It is an instance of DS\_001 Generic Date This is the time of the stop and search It is an instance of DS\_002 Generic Time This is the ethnicity as defined by the person being stopped and searched It is an instance of DS\_038 Ethnicity This is the ethnicity as defined by the officer stopping and searching

Given Name

Surname

Date of Birth

Age

Place of Birth

Date of Search

Time of Search

Self-defined Ethnicity

Officer-defined Ethnicity

[Image]

|                   | Search Officer  the individual  This is an instance of  P_070 Collar  Number 2. At least one of the following location component parts must be  included:  Stop Location - Address  Address (DS_005, DS_007, DS_008,  DS_009, DS_010)  Stop Location - Post Code  DS_010 Postcode  Stop Location - Geometric  DS_015 Location Longitude, DS_014  Latitude  Stop Location - Area  DS_016 Location Area   | It is an instance of  DS_038 Ethnicity This is the officer stopping and searching                                                                                                                         |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation  Rules | 1. Date of Incident  must not be in the future  2. Time of Incident  must not be in the future  3. Time of Incident  is the time the incident is reported  4. See Component Standards for all components.                                                                                                                                                                                               | 1. Date of Incident  must not be in the future  2. Time of Incident  must not be in the future  3. Time of Incident  is the time the incident is reported  4. See Component Standards for all components. |
| Related  Terms    |                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                           |
| Notes             |  See General Validation Notes                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                           |

## Description

## Component Parts

[Image]

## 5.5: Safeguarding

| Ref No:   | E_005   | Entity   | Safeguarding   | Safeguarding    |
|-----------|---------|----------|----------------|-----------------|
| Class:    | Event   | Owner:   |                | Steward:        |
| Version:  |         | Status:  | Draft          | Approval  Date: |

## Minimum Completeness Requirement

The term safeguarding covers a range of activities which is aimed at supporting adults to exercise their basic right to live a life free from the fear or reality of abuse, regardless of where they live or the situation they are in.

## Drawn from College of Policing

Denotes measures to protect the health and well-being and human rights of individuals, which allow people - especially children, young people and vulnerable adults to live free from abuse, harm and neglect.

1. The following component parts are mandatory:

Safeguarding Victim

P\_004 Victim

Safeguarding Suspect

P\_002 Suspect - Known

Repeat Victim

DS\_093 Repeat Victim

Repeat Offender

DS\_094 Repeat Offender

Any children present?

DS\_095 Children Present

2. At least one of the following location component parts must be included:

Incident Location - Address

Address (DS\_005, DS\_007, DS\_008, DS\_009, DS\_010)

Incident Location - Post Code

Incident Location - Geometric

Incident Location - Area

DS\_010 Postcode DS\_015 Location Longitude, DS\_014 Latitude L\_004 Location - Area

[Image]

| Validation  Rules   | 1. See Component Standards for all components.   |
|---------------------|--------------------------------------------------|
| Related  Terms      |                                                  |
| Notes               |  See General Validation Notes                   |

Description

## Component Parts

[Image]

## 5.6: Anti-social Behaviour

| Ref No:   | E_006   | Entity   | Anti-social Behaviour   | Anti-social Behaviour   |
|-----------|---------|----------|-------------------------|-------------------------|
| Class:    | Event   | Owner:   |                         | Steward:                |
| Version:  |         | Status:  | Draft                   | Approval  Date:         |

## Minimum Completeness Requirement

The Crime and Disorder Act (1998) definition of anti-social behaviour (ASB) is widely used by Crime and Disorder Reduction Partnerships (CDRPs) and Community Safety Partnerships (CSPs) involved in the RDS study. It defines ASB as follows: 'Acting in a manner that caused or was likely to cause harassment, alarm or distress to one or more persons not of the same household as (the defendant).'

' Anti-social behaviour' means:

- (a) conduct that has caused, or is likely to cause, harassment, alarm or distress to any person,
- (b) conduct capable of causing nuisance or annoyance to a person in relation to that person's occupation of residential premises, or
- (c) conduct capable of causing housing-related nuisance or annoyance to any person

Anti-social Behaviour, Crime and Policing Act 2014 (legislation.gov.uk)

1. The following component parts are mandatory:
2. At least one of the following location component parts:

ASB Reporting Person

P\_018 Person Reporting DS\_106 ASB Class DS\_107 ASB Type DS\_108 ASB Questionnaire DS\_093 Repeat Victim

ASB Class

ASB Type

ASB Questionnaire?

Repeat Victim

[Image]

|                   | Incident Location - Address                                                           | Address (DS_005, DS_007, DS_008,  DS_009, DS_010)                                                   |
|-------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
|                   | Incident Location - Postcode  Incident Location - Geometric  Incident Location - Area | DS_010 Postcode  DS_014 Location - Latitude,   DS_015 Location - Longitude,  DS_004 Location - Area |
| Validation  Rules | 1. See Component Standards for all components.                                        | 1. See Component Standards for all components.                                                      |
| Related  Terms    |                                                                                       |                                                                                                     |
| Notes             |  See General Validation Notes                                                        |  See General Validation Notes                                                                      |

## Summary of all minimum POLE data standards

|   Serial No | Minimum Data Standard   |
|-------------|-------------------------|
|         001 | Generic Date            |
|         003 | Expected Due Date       |
|         004 | Country                 |
|         005 | Site Location           |
|         006 | Premises                |
|         007 | Street                  |
|         008 | Town                    |
|         009 | County                  |
|         010 | Post Code               |
|         011 | Property UPRN           |
|         012 | Business Name           |
|         013 | Unit Number             |
|         014 | Location - Latitude     |
|         015 | Location - Longitude    |
|         016 | Location - Area         |
|         031 | Given Name              |
|         032 | Surname                 |
|         033 | Alias / Nickname        |
|         034 | Date of Birth           |
|         035 | Place of Birth          |

[Image]

|   037 | Gender                         |
|-------|--------------------------------|
|   038 | Self-defined ethnicity         |
|   039 | Build                          |
|   040 | Complexion                     |
|   041 | Eye Colour Left                |
|   042 | Eye Colour Right               |
|   043 | Distinguishing Feature         |
|   046 | Hair Colour                    |
|   047 | Person Relationship            |
|   051 | Telephone Type Code            |
|   052 | Telephone Country              |
|   053 | Telephone Number               |
|   054 | Email Address                  |
|   055 | Social Media Tag               |
|   056 | UK Passport Number             |
|   057 | Foreign Passport Number        |
|   058 | Passport Validity              |
|   059 | Passport Country               |
|   060 | National Insurance Number      |
|   061 | UK Driving Licence Number      |
|   062 | Foreign Driving Licence Number |
|   063 | Driving Licence Country        |
|   065 | Vehicle - VRM                  |

[Image]

|   066 | Vehicle - Make                 |
|-------|--------------------------------|
|   067 | Vehicle - Model                |
|   068 | Vehicle - Shape                |
|   069 | Vehicle - Colour               |
|   070 | Collar Number                  |
|   071 | Criminal Records Office Number |
|   072 | Police National Computer ID    |
|   073 | Arrest Summons Number          |
|   074 | Home Office Classification     |
|   075 | Verification of Death          |
|   076 | Date of Death                  |
|   078 | Crime Type                     |
|   080 | Offence Type (Offence Code)    |
|   083 | Crime Outcome                  |
|   084 | Crime Status / Clear Up Method |
|   086 | Arrest Reason                  |
|   088 | MO (Modus Operandi)            |
|   091 | NSIR Opening Code              |
|   092 | NSIR Closing Code              |
|   093 | Repeat Victim                  |
|   094 | Repeat Offender                |
|   095 | Children Present               |
|   096 | Hate Crime                     |

[Image]

|   097 | Property - Category    |
|-------|------------------------|
|   098 | Property - Description |
|   099 | Unique ID Number Type  |
|   100 | Unique Number          |
|   101 | Photograph Description |
|   102 | Photograph             |
|   103 | Date of Photograph     |
|   105 | Stop Nature            |
|   106 | ASB Class              |
|   107 | ASB Type               |
|   108 | ASB Questionnaire      |
|   109 | Telephone Extension    |
|   110 | Correct Checks         |
|   111 | SAFE number            |

[Image]

## 6. POLE Data Attribute Standards

## 001: Generic Date

| 001                      |                                                                                                   |
|--------------------------|---------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                            |
| Entity Group             | Generic                                                                                           |
| Attribute Name           | Generic Date                                                                                      |
| Attribute Description    | Expected due date for unborn                                                                      |
| Standard Type            | International                                                                                     |
| Minimum Standard         | Yes                                                                                               |
| Protected Characteristic | No                                                                                                |
| Version                  | TBC                                                                                               |
| Approval Date            | TBC                                                                                               |
| Minimum                  | 10                                                                                                |
| Maximum                  | 10                                                                                                |
| Default                  |                                                                                                   |
| Value Range              |                                                                                                   |
| Validation               | 1. Numeric  2. Must be a valid date in the format YYYY-MM-DD  3. Leading zeros should be included |
| Board                    | ISO                                                                                               |
| Owner                    | ISO 8601                                                                                          |
| Steward                  |                                                                                                   |
| Based On                 | ISO 8601                                                                                          |

## 003: Expected Due Date

| 003                      | 003                                                   |
|--------------------------|-------------------------------------------------------|
| POLE Class               | Person                                                |
| Entity Group             | Generic                                               |
| Attribute Name           | Expected Due Date                                     |
| Attribute Description    | Expected due date for unborn                          |
| Standard Type            | International                                         |
| Minimum Standard         | Yes                                                   |
| Protected Characteristic | Yes - Association exists with 'Pregnancy & Maternity' |
| Version                  | TBC                                                   |
| Approval Date            | TBC                                                   |

| Minimum     | 10                                                                                                                                        |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Maximum     | 10                                                                                                                                        |
| Default     |                                                                                                                                           |
| Value Range |                                                                                                                                           |
| Validation  | 1. Numeric  2. Must be a valid date in the format YYYY-MM-DD  3. The date should not be in the past  4 . Leading zeros should be included |
| Board       | ISO                                                                                                                                       |
| Owner       | ISO 8601                                                                                                                                  |
| Steward     |                                                                                                                                           |
| Based On    | ISO 8601                                                                                                                                  |

## 004: Country code

| 004                      |                                                                           |
|--------------------------|---------------------------------------------------------------------------|
| POLE Class               | Location                                                                  |
| Entity Group             | Address                                                                   |
| Attribute Name           | Country Code                                                              |
| Attribute Description    | A unique code representing a country                                      |
| Standard Type            | International                                                             |
| Minimum Standard         | Yes                                                                       |
| Protected Characteristic | No                                                                        |
| Version                  | TBC                                                                       |
| Approval Date            | TBC                                                                       |
| Minimum                  | 03                                                                        |
| Maximum                  | 03                                                                        |
| Default                  | GBR                                                                       |
| Value Range              |                                                                           |
| Validation               | 1. Alphabetic  2. 3 Letter code  3. Code must be on the BS EN 3166-1 List |
| Board                    | ISO                                                                       |
| Owner                    | ISO BS EN 3166                                                            |
| Steward                  |                                                                           |
| Based On                 | ISO BS EN 3166-1                                                          |

[Image]

## 005: Site Location

| 005                      |                                                                                                  |
|--------------------------|--------------------------------------------------------------------------------------------------|
| POLE Class               | Location                                                                                         |
| Entity Group             | Address                                                                                          |
| Attribute Name           | Site Location                                                                                    |
| Attribute Description    | Floor,Flat or House Number                                                                       |
| Standard Type            | National                                                                                         |
| Minimum Standard         | Yes                                                                                              |
| Protected Characteristic | No                                                                                               |
| Version                  | TBC                                                                                              |
| Approval Date            | TBC                                                                                              |
| Minimum                  | 01                                                                                               |
| Maximum                  | 05                                                                                               |
| Default                  |                                                                                                  |
| Value Range              |                                                                                                  |
| Validation               | 1. Alphanumeric  2. Ground Floor = '0'  3. Either floor or flat number should be used - not both |
| Board                    | Royal Mail (ONS Postcode Directory (ONSPD))                                                      |
| Owner                    | Royal Mail                                                                                       |
| Steward                  |                                                                                                  |
| Based On                 |                                                                                                  |

## 006: Premises

| 006                   | 006                     |
|-----------------------|-------------------------|
| POLE Class            | Location                |
| Entity Group          | Address                 |
| Attribute Name        | Premises                |
| Attribute Description | Premises Name or Number |
| Standard Type         | National                |
| Minimum Standard      | Yes                     |

[Image]

| Protected Characteristic   | No                                          |
|----------------------------|---------------------------------------------|
| Version                    | TBC                                         |
| Approval Date              | TBC                                         |
| Minimum                    | 01                                          |
| Maximum                    | 35                                          |
| Default                    |                                             |
| Value Range                |                                             |
| Validation                 | 1. Alphanumeric                             |
| Board                      | Royal Mail (ONS Postcode Directory (ONSPD)) |
| Owner                      | Royal Mail                                  |
| Steward                    |                                             |
| Based On                   |                                             |

## 007: Street

| 007                      |                                             |
|--------------------------|---------------------------------------------|
| POLE Class               | Location                                    |
| Entity Group             | Address                                     |
| Attribute Name           | Street                                      |
| Attribute Description    | Street name                                 |
| Standard Type            | National                                    |
| Minimum Standard         | Yes                                         |
| Protected Characteristic | No                                          |
| Version                  | TBC                                         |
| Approval Date            | TBC                                         |
| Minimum                  | 01                                          |
| Maximum                  | 35                                          |
| Default                  |                                             |
| Value Range              |                                             |
| Validation               | 1. Alphanumeric                             |
| Board                    | Royal Mail (ONS Postcode Directory (ONSPD)) |
| Owner                    | Royal Mail                                  |
| Steward                  |                                             |
| Based On                 | ONS Postcode Directory (ONSPD)              |

## 008: Town

| 008        |          |
|------------|----------|
| POLE Class | Location |

[Image]

| Entity Group             | Address                                     |
|--------------------------|---------------------------------------------|
| Attribute Name           | Town                                        |
| Attribute Description    | Town name                                   |
| Standard Type            | National                                    |
| Minimum Standard         | Yes                                         |
| Protected Characteristic | No                                          |
| Version                  | TBC                                         |
| Approval Date            | TBC                                         |
| Minimum                  | 01                                          |
| Maximum                  | 35                                          |
| Default                  |                                             |
| Value Range              |                                             |
| Validation               | 1. Alphanumeric                             |
| Board                    | Royal Mail (ONS Postcode Directory (ONSPD)) |
| Owner                    | Royal Mail                                  |
| Steward                  |                                             |
| Based On                 | ONS Postcode Directory (ONSPD)              |

## 009: County Name

| 009                      |                                             |
|--------------------------|---------------------------------------------|
| POLE Class               | Location                                    |
| Entity Group             | Address                                     |
| Attribute Name           | County                                      |
| Attribute Description    | County name                                 |
| Standard Type            | National                                    |
| Minimum Standard         | Yes                                         |
| Protected Characteristic | No                                          |
| Version                  | TBC                                         |
| Approval Date            | TBC                                         |
| Minimum                  | 01                                          |
| Maximum                  | 35                                          |
| Default                  |                                             |
| Value Range              |                                             |
| Validation               | 1. Alphanumeric                             |
| Board                    | Royal Mail (ONS Postcode Directory (ONSPD)) |
| Owner                    | Royal Mail                                  |
| Steward                  |                                             |

[Image]

## Based On

## ONS Postcode Directory (ONSPD)

## 010: Post Code

| 010                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Location                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Entity Group             | Address                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Attribute Name           | Post Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Attribute Description    | The code allocated by the Post Office to identify a group of postal  delivery points                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Standard Type            | National                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Version                  | TBC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Minimum                  | 06                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Maximum                  | 08                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Default                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Value Range              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Validation               | 1. Only valid UK postcodes should be used in this field, invalid and  foreign postcodes / zip codes are to be placed in the fifth line of  address - 'County'   2. The outward code can be 2, 3 or 4 characters followed by a space  and the inward code, which is 3 characters and is always NAA  3. The outward code has seven valid formats, AN, ANN, AAN, AANN,  ANA, AANA and AAA  4. The letters I, J and Z are not used in the first position  5. The letters I, J and Z are not used in the second position  6. The only letters to appear in the third position are A, B, C, D, E, F,  G, H, J, K, S, T, U and W  7. The only letters to appear in the fourth position are A, B, E, H, M,  N, P, R, V, W, X and Y  8. The second half of the Postcode is always NAA and the letters C, I,  K, M, O and V are never used  9. GIR 0AA is the only Postcode that doesn't comply with the above  validation rules. |

[Image]

| Board    | Royal Mail (ONS Postcode Directory (ONSPD))   |
|----------|-----------------------------------------------|
| Owner    | Royal Mail                                    |
| Steward  |                                               |
| Based On | ONS Postcode Directory (ONSPD)                |

## 011: Property UPRN

| 011                      |                                                                                                                                                                                                                                                                                                                                            |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Location                                                                                                                                                                                                                                                                                                                                   |
| Entity Group             | Address                                                                                                                                                                                                                                                                                                                                    |
| Attribute Name           | Property UPRN                                                                                                                                                                                                                                                                                                                              |
| Attribute Description    | A Unique Property Reference Number (UPRN) is a unique numeric  identifier for every addressable location in Great Britain, found in  OS's Address Base products. An addressable location may be any kind  of building, residential or commercial, or it may be an object that  might not have a 'postal ' address - such as a bus shelter. |
| Standard Type            | National                                                                                                                                                                                                                                                                                                                                   |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                                                        |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                                                         |
| Version                  | TBC                                                                                                                                                                                                                                                                                                                                        |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                                                        |
| Minimum                  | 12                                                                                                                                                                                                                                                                                                                                         |
| Maximum                  | 12                                                                                                                                                                                                                                                                                                                                         |
| Default                  |                                                                                                                                                                                                                                                                                                                                            |
| Value Range              |                                                                                                                                                                                                                                                                                                                                            |
| Validation               | A Unique Property Reference Number (UPRN) is a unique numeric  identifier for every addressable location in Great Britain, found in  OS's Address Base products. An addressable location may be any kind  of building, residential or commercial, or it may be an object that  might not have a 'postal' address - such as a bus shelter.  |
| Board                    | Ordnance Survey                                                                                                                                                                                                                                                                                                                            |
| Owner                    | Ordnance Survey                                                                                                                                                                                                                                                                                                                            |
| Steward                  |                                                                                                                                                                                                                                                                                                                                            |
| Based On                 | Ordnance Survey                                                                                                                                                                                                                                                                                                                            |

[Image]

## Additional commentary

National Statistics UPRN Lookup (NSUL) - Uses the NSUL allocates source statistics at address level to a wide range of higher geographies in conjunction with Ordnance Survey's AddressBase® product. The NSUL allocates each current GB address to an Output Area (OA) using the UPRN

## 012: Business Name

| 012                      |                  |
|--------------------------|------------------|
| POLE Class               | Object           |
| Entity Group             | Business Name    |
| Attribute Name           | Property UPRN    |
| Attribute Description    | Name of Business |
| Standard Type            | Free text        |
| Minimum Standard         | Yes              |
| Protected Characteristic | No               |
| Version                  | TBC              |
| Approval Date            | TBC              |
| Minimum                  | 01               |
| Maximum                  | 35               |
| Default                  |                  |
| Value Range              |                  |
| Validation               | 1. Alphanumeric  |
| Board                    | N/A              |
| Owner                    | None             |
| Steward                  |                  |
| Based On                 | None             |

## 013: Unit Number

| 013            |             |
|----------------|-------------|
| POLE Class     | Location    |
| Entity Group   | Address     |
| Attribute Name | Unit Number |

[Image]

| Attribute Description    | Business unit number   |
|--------------------------|------------------------|
| Standard Type            | Free text              |
| Minimum Standard         | Yes                    |
| Protected Characteristic | No                     |
| Version                  | TBC                    |
| Approval Date            | TBC                    |
| Minimum                  | 01                     |
| Maximum                  | 35                     |
| Default                  |                        |
| Value Range              |                        |
| Validation               | 1. Alphanumeric        |
| Board                    | N/A                    |
| Owner                    | None                   |
| Steward                  |                        |
| Based On                 | None                   |

## 014: Location Latitude

| 014                      |                                                                                                                              |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Location                                                                                                                     |
| Entity Group             | Address                                                                                                                      |
| Attribute Name           | Location - Latitude                                                                                                          |
| Attribute Description    | A measure of how far a location is either north or south of the  equator                                                     |
| Standard Type            | International                                                                                                                |
| Minimum Standard         | Yes                                                                                                                          |
| Protected Characteristic | No                                                                                                                           |
| Version                  | TBC                                                                                                                          |
| Approval Date            | TBC                                                                                                                          |
| Minimum                  | 10                                                                                                                           |
| Maximum                  | 14                                                                                                                           |
| Default                  |                                                                                                                              |
| Value Range              | 90°00′00.0"S - 90°00′00.0"N  -90°00′00.0" - +90°00′00.0"                                                                     |
| Validation               | 1. Alphanumeric  2. 0 = Equator  3. Value must be preceded by '+' or '-' (+ = Northern Hemisphere, - =  Southern Hemisphere) |

[Image]

|          | OR  followed by 'N' (For north of the Equator) and 'W' (For south of the  Equator)  4. Formats = DD°MM′SS.S″  5. Integer element is a fixed length therefore leading 0's MUST be  included              |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board    | ISO                                                                                                                                                                                                     |
| Owner    | ISO                                                                                                                                                                                                     |
| Steward  |                                                                                                                                                                                                         |
| Based On | ISO6709 - Standard representation of geographic point location by  coordinates. It is the international standard for representation of  latitude, longitude and altitude for geographic point locations |

## 015: Location - Longitude

| 015                      |                                                                                                                                                |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Location                                                                                                                                       |
| Entity Group             | Address                                                                                                                                        |
| Attribute Name           | Location - Longitude                                                                                                                           |
| Attribute Description    | A measure of how far a location is either east or west of the equator                                                                          |
| Standard Type            | International                                                                                                                                  |
| Minimum Standard         | Yes                                                                                                                                            |
| Protected Characteristic | No                                                                                                                                             |
| Version                  | TBC                                                                                                                                            |
| Approval Date            | TBC                                                                                                                                            |
| Minimum                  | 11                                                                                                                                             |
| Maximum                  | 15                                                                                                                                             |
| Default                  |                                                                                                                                                |
| Value Range              | 180°00′00.0″W - 180°00′00.0″E  -180°00′00.0″ - +180°00′00.0″                                                                                   |
| Validation               | 1. Alphanumeric  2. 0 = Prime Meridian  3. Value must be preceded by '+' or '-' (+ = East of Prime Meridian, - =   West of Prime Meridian)  OR |

[Image]

|          | followed by 'E' (For east of Prime Meridian) and 'W' (For west of  Prime Meridian)  4. Formats = DDD°MM′SS.S″  5. Integer element is a fixed length therefore leading 0's MUST be  included             |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board    | ISO                                                                                                                                                                                                     |
| Owner    | ISO                                                                                                                                                                                                     |
| Steward  |                                                                                                                                                                                                         |
| Based On | ISO6709 - Standard representation of geographic point location by  coordinates. It is the international standard for representation of  latitude, longitude and altitude for geographic point locations |

## 016: Location - Area

| 016                      |                                                                                                |
|--------------------------|------------------------------------------------------------------------------------------------|
| POLE Class               | Location                                                                                       |
| Entity Group             | Address                                                                                        |
| Attribute Name           | Location - Area                                                                                |
| Attribute Description    | A short description of a location to be used in the absence of  postcode or geometric location |
| Standard Type            | International                                                                                  |
| Minimum Standard         | Yes                                                                                            |
| Protected Characteristic | No                                                                                             |
| Version                  | TBC                                                                                            |
| Approval Date            | TBC                                                                                            |
| Minimum                  | 1                                                                                              |
| Maximum                  | 100                                                                                            |
| Default                  |                                                                                                |
| Value Range              | Free text                                                                                      |
| Validation               | 1. Alphanumeric                                                                                |
| Board                    | ISO                                                                                            |

[Image]

| Owner                 | ISO                                                                                           |
|-----------------------|-----------------------------------------------------------------------------------------------|
| Steward               |                                                                                               |
| Based On              | ISO6709 - Standard representation of geographic point location by  coordinates                |
| Additional commentary | We have retained as free text with guidance on what should be  included in Entity validation. |

## 031: Given Name

| 031                      |                                              |
|--------------------------|----------------------------------------------|
| POLE Class               | Person                                       |
| Entity Group             | Person Description                           |
| Attribute Name           | Given Name                                   |
| Attribute Description    | The forename(s) or given name(s) of a person |
| Standard Type            | Free text                                    |
| Minimum Standard         | Yes                                          |
| Protected Characteristic | No                                           |
| Version                  | TBC                                          |
| Approval Date            | TBC                                          |
| Minimum                  | 01                                           |
| Maximum                  | 35                                           |
| Default                  |                                              |
| Value Range              |                                              |
| Validation               | 1. Alphanumeric  2. No consecutive spaces    |
| Board                    | NSAB                                         |
| Owner                    | NPCC - IMORCC                                |
| Steward                  |                                              |
| Based On                 | CJS Data source (e-GIF and BSEN 7372: 1993)  |

## 032: Surname

| 032                   | 032                                                                                                  |
|-----------------------|------------------------------------------------------------------------------------------------------|
| POLE Class            | Person                                                                                               |
| Entity Group          | Person Description                                                                                   |
| Attribute Name        | Surname                                                                                              |
| Attribute Description | Part of a person's name which is used to describe family, clan, tribal  group or marital association |
| Standard Type         | Free text                                                                                            |

[Image]

| Minimum Standard         | Yes                                         |
|--------------------------|---------------------------------------------|
| Protected Characteristic | No                                          |
| Version                  | TBC                                         |
| Approval Date            | TBC                                         |
| Minimum                  | 01                                          |
| Maximum                  | 35                                          |
| Default                  |                                             |
| Value Range              |                                             |
| Validation               | 1. Alphanumeric  2. No consecutive spaces   |
| Board                    | NSAB                                        |
| Owner                    | NPCC - IMORCC                               |
| Steward                  |                                             |
| Based On                 | CJS Data source (e-GIF and BSEN 7372: 1993) |

## 033: Alias / Nickname

| 033                   | 033                                                                                                                                                                                                                                                                                                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class            | Person                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Entity Group          | Person Description                                                                                                                                                                                                                                                                                                                                                                                                           |
| Attribute Name        | Nickname                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Attribute Description | A name a person is also known as or referred to by others or  themselves.  This could be a part of a person's name which is used to describe  family, clan, tribal group or marital association but could also be a  previous name, a name that relates to a physical characteristic of a  person, a previous incident a person was involved in, a name that has  been used to hide the true identity of a person and so on. |
| Standard Type         | Free text                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Minimum Standard      | Yes                                                                                                                                                                                                                                                                                                                                                                                                                          |

[Image]

| Protected Characteristic   | No                                        |
|----------------------------|-------------------------------------------|
| Version                    | TBC                                       |
| Approval Date              | TBC                                       |
| Minimum                    | 01                                        |
| Maximum                    | 35                                        |
| Default                    |                                           |
| Value Range                |                                           |
| Validation                 | 1. Alphanumeric  2. No consecutive spaces |
| Board                      | NSAB                                      |
| Owner                      | NPCC - IMORCC                             |
| Steward                    |                                           |
| Based On                   | None                                      |

## 034: Date of Birth

| 034                      |                                                                                                                                                                                                                                  |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                                                                                                                           |
| Entity Group             | Person Description                                                                                                                                                                                                               |
| Attribute Name           | Date of Birth                                                                                                                                                                                                                    |
| Attribute Description    | The date of birth of a person                                                                                                                                                                                                    |
| Standard Type            | International                                                                                                                                                                                                                    |
| Minimum Standard         | Yes                                                                                                                                                                                                                              |
| Protected Characteristic | Yes - Association exists with 'Age'                                                                                                                                                                                              |
| Version                  | TBC                                                                                                                                                                                                                              |
| Approval Date            | TBC                                                                                                                                                                                                                              |
| Minimum                  | 10                                                                                                                                                                                                                               |
| Maximum                  | 10                                                                                                                                                                                                                               |
| Default                  |                                                                                                                                                                                                                                  |
| Value Range              |                                                                                                                                                                                                                                  |
| Validation               | 1. Date of Birth must not be in the future  2. Date of Birth must not be today's date  3. Date of Birth must not be later than person's date of death, where  held  4. Age at time of reporting must not be more than 120 years. |
| Board                    | ISO                                                                                                                                                                                                                              |
| Owner                    | ISO                                                                                                                                                                                                                              |

[Image]

| Steward   |         |
|-----------|---------|
| Based On  | ISO8601 |

## 035: Place of Birth

| 035                      |                                                                                                                                                                 |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                                                          |
| Entity Group             | Person Description                                                                                                                                              |
| Attribute Name           | Place of Birth                                                                                                                                                  |
| Attribute Description    | A person's town of birth                                                                                                                                        |
| Standard Type            | Free text                                                                                                                                                       |
| Minimum Standard         | Yes                                                                                                                                                             |
| Protected Characteristic | Potential influence on protected characteristic 'Age'                                                                                                           |
| Version                  | TBC                                                                                                                                                             |
| Approval Date            | TBC                                                                                                                                                             |
| Minimum                  | 01                                                                                                                                                              |
| Maximum                  | 35                                                                                                                                                              |
| Default                  |                                                                                                                                                                 |
| Value Range              |                                                                                                                                                                 |
| Validation               | 1. Alphanumeric                                                                                                                                                 |
| Board                    | NSAB                                                                                                                                                            |
| Owner                    | Royal Mail                                                                                                                                                      |
| Steward                  |                                                                                                                                                                 |
| Based On                 | ONS Postcode Directory (ONSPD)                                                                                                                                  |
| Additional commentary    | The ONS publishes major towns and cities with 9 digit reference  codes in the UK. If this is used for international town of birth - free  text may be necessary |

## 037: Gender

| 037                   | 037                          |
|-----------------------|------------------------------|
| POLE Class            | Person                       |
| Entity Group          | Person Description           |
| Attribute Name        | Gender                       |
| Attribute Description | Gender Classification        |
| Standard Type         | Police national to be agreed |

[Image]

| Minimum Standard         | Yes                                                                                     |
|--------------------------|-----------------------------------------------------------------------------------------|
| Protected Characteristic | Yes - Association exists with 'Sex' and 'Gender Reassignment'                           |
| Version                  | TBC                                                                                     |
| Approval Date            | TBC                                                                                     |
| Minimum                  | 01                                                                                      |
| Maximum                  | 35                                                                                      |
| Default                  |                                                                                         |
| Value Range              | Male   Female  Trans Male  Trans Female  Non-Binary  Intersex  Not Specified  Not Known |
| Validation               | 1. Alphanumeric                                                                         |
| Board                    | NSAB                                                                                    |
| Owner                    | NPCC - DIVERSITY, EQUALITY & INCLUSION (LGBT)                                           |
| Steward                  |                                                                                         |
| Based On                 | Census 21 guidance                                                                      |

## 038: Self Defined Ethnicity code

| 038                      |                                                                                                                      |
|--------------------------|----------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                               |
| Entity Group             | Person Description                                                                                                   |
| Attribute Name           | Self-defined ethnicity code                                                                                          |
| Attribute Description    | Ethnicity of a person (Self-defined)                                                                                 |
| Standard Type            | Police national to be agreed                                                                                         |
| Minimum Standard         | Yes                                                                                                                  |
| Protected Characteristic | Yes - Direct alignment to 'Race'                                                                                     |
| Version                  | TBC                                                                                                                  |
| Approval Date            | TBC                                                                                                                  |
| Minimum                  | 01                                                                                                                   |
| Maximum                  | 35                                                                                                                   |
| Default                  |                                                                                                                      |
| Value Range              | 1.White ­English / Welsh / Scottish / Northern Irish / British   2. White Irish   3. White  Gypsy or Irish Traveller |

[Image]

|            | 4. White ­ Any other White background   5. Mixed ­White and Black Caribbean   6. Mixed ­White and Black African   7. Mixed ­White and Asian   8.Mixed ­Any other Mixed / multiple ethnic background   9. Asian­ Indian   10. Asian ­Pakistani   11. Asian ­ Bangladeshi   12. Asian ­Chinese  13. Asian ­Any other Asian background   14. Black ­ African 15. Black ­ Caribbean 16.Black ­Any other Black /  African / Caribbean background   17. Other ­ Arab   18. Other ­ Any other ethnic group 19. Prefer not to say Unknown   |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation | 1. Numeric Values 1 - 18  2. ONS Ethnicity  code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Board      | NSAB                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Owner      | NPCC - DIVERSITY, EQUALITY & INCLUSION (Race, Religion & Belief  Portfolio)                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Steward    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Based On   | ONS 18+1 Ethnicity Code (also used in Workforce Data National  Standards)                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## 112: Observed Ethnicity code

| 112                      | 112                                                                                                                    |
|--------------------------|------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                 |
| Entity Group             | Person Description                                                                                                     |
| Attribute Name           | Observed ethnicity code                                                                                                |
| Attribute Description    | The seven values (6+1) used in various Police applications to describe  a person's ethnic appearance to a third party. |
| Standard Type            | Police national to be agreed                                                                                           |
| Minimum Standard         | Yes                                                                                                                    |
| Protected Characteristic | Yes - Direct alignment to 'Race'                                                                                       |
| Version                  | TBC                                                                                                                    |
| Approval Date            | TBC                                                                                                                    |
| Minimum                  | 02                                                                                                                     |
| Maximum                  | 35                                                                                                                     |
| Default                  |                                                                                                                        |

[Image]

| Value Range   | 0 not recorded/not known  1 White - North European  2 White - South European  3 Black  4 Asian  5 Chinese, Japanese or any other Southeast Asian  6 Arabic or North African  7.Mixed ­Any other Mixed / multiple ethnic background   |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validation    | 1. Numeric Values 0 - 7.  2. ONS ethnicity code                                                                                                                                                                                      |
| Board         | NSAB                                                                                                                                                                                                                                 |
| Owner         | NPCC - DIVERSITY, EQUALITY & INCLUSION (Race, Religion & Belief  Portfolio)                                                                                                                                                          |
| Steward       |                                                                                                                                                                                                                                      |
| Based On      | None                                                                                                                                                                                                                                 |

## 039: Person Build

| 039                      |                                                      |
|--------------------------|------------------------------------------------------|
| POLE Class               | Person                                               |
| Entity Group             | Person Description                                   |
| Attribute Name           | Person Build                                         |
| Attribute Description    | Person's body description                            |
| Standard Type            | Police national to be agreed                         |
| Minimum Standard         | Yes                                                  |
| Protected Characteristic | No                                                   |
| Version                  | TBC                                                  |
| Approval Date            | TBC                                                  |
| Minimum                  | 03                                                   |
| Maximum                  | 35                                                   |
| Default                  |                                                      |
| Value Range              | Medium  Broad  Heavy  Thin  Fat  Stocky  Slim  Large |

[Image]

|            | Slight  Small  Proportionate  U/K                      |
|------------|--------------------------------------------------------|
| Validation | 1. Alphanumeric                                        |
| Board      | NSAB                                                   |
| Owner      | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward    |                                                        |
| Based On   | PND - PersonBodyDescriptionBuildList                   |

## 040: Person's Complexion

| 040                      |                                                                                  |
|--------------------------|----------------------------------------------------------------------------------|
| POLE Class               | Person                                                                           |
| Entity Group             | Person Description                                                               |
| Attribute Name           | Person's complexion                                                              |
| Attribute Description    | The natural colour, texture, and appearance of the skin, especially of  the face |
| Standard Type            | Police national to be agreed                                                     |
| Minimum Standard         | Yes                                                                              |
| Protected Characteristic | No                                                                               |
| Version                  | TBC                                                                              |
| Approval Date            | TBC                                                                              |
| Minimum                  | 01                                                                               |
| Maximum                  | 35                                                                               |
| Default                  |                                                                                  |
| Value Range              | Fresh  Albino  Ruddy  Fair  Pale  Tanned  allow  Dark  Swarthy  U/K              |
| Validation               | 1. Alphanumeric                                                                  |
| Board                    | NSAB                                                                             |
| Owner                    | NPCC - CRIME OPS (Performance and Standards portfolio)                           |

[Image]

| Steward   |                                           |
|-----------|-------------------------------------------|
| Based On  | PND - PersonBodyDescriptionComplexionList |

## 041: Eye Colour Left

| 041                      |                                                        |
|--------------------------|--------------------------------------------------------|
| POLE Class               | Person                                                 |
| Entity Group             | Person Description                                     |
| Attribute Name           | Eye Colour Left                                        |
| Attribute Description    | Colour of person's LEFT eye                            |
| Standard Type            | Police national to be agreed                           |
| Minimum Standard         | Yes                                                    |
| Protected Characteristic | No                                                     |
| Version                  | TBC                                                    |
| Approval Date            | TBC                                                    |
| Minimum                  | 01                                                     |
| Maximum                  | 35                                                     |
| Default                  |                                                        |
| Value Range              | Blue  Brown  Green  Grey  Hazel  U/K                   |
| Validation               | 1. Alphanumeric                                        |
| Board                    | NSAB                                                   |
| Owner                    | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward                  |                                                        |
| Based On                 | PND - PersonBodyDescriptionEyeLeftColourList           |

## 042: Eye Colour Right

| 042                   | 042                          |
|-----------------------|------------------------------|
| POLE Class            | Person                       |
| Entity Group          | Person Description           |
| Attribute Name        | Eye colour right             |
| Attribute Description | Colour of person's RIGHT eye |
| Standard Type         | Police national to be agreed |
| Minimum Standard      | Yes                          |

[Image]

| Protected Characteristic   | No                                                        |
|----------------------------|-----------------------------------------------------------|
| Version                    | TBC                                                       |
| Approval Date              | TBC                                                       |
| Minimum                    | 01                                                        |
| Maximum                    | 35                                                        |
| Default                    |                                                           |
| Value Range                | Blue  Brown  Green  Grey  Hazel  U/K  Unmapped Local Code |
| Validation                 | 1. Alphanumeric                                           |
| Board                      | NSAB                                                      |
| Owner                      | NPCC - CRIME OPS (Performance and Standards portfolio)    |
| Steward                    |                                                           |
| Based On                   | PND - PersonBodyDescriptionEyeRightColourList             |

## 043: Distinguishing Feature

| 043                      |                                           |
|--------------------------|-------------------------------------------|
| POLE Class               | Person                                    |
| Entity Group             | Person Description                        |
| Attribute Name           | Distinguishing feature                    |
| Attribute Description    | Class of distinguishing feature           |
| Standard Type            | Police national to be agreed              |
| Minimum Standard         | Yes                                       |
| Protected Characteristic | No                                        |
| Version                  | TBC                                       |
| Approval Date            | TBC                                       |
| Minimum                  | 01                                        |
| Maximum                  | 35                                        |
| Default                  |                                           |
| Value Range              | Lacking  Mark  Peculiar  Pierced  Scarred |

[Image]

|            | Tattoo  Unmapped Local Code                            |
|------------|--------------------------------------------------------|
| Validation | 1. Alphanumeric                                        |
| Board      | NSAB                                                   |
| Owner      | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward    |                                                        |
| Based On   | PND - PersonBodyDistinguishingFeatureFeatureList       |

## 046: Hair Colour

| 046                      |                                                                                                                              |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                       |
| Entity Group             | Person Description                                                                                                           |
| Attribute Name           | Hair Colour                                                                                                                  |
| Attribute Description    | Colour of hair on a person's head                                                                                            |
| Standard Type            | Police national to be agreed                                                                                                 |
| Minimum Standard         | Yes                                                                                                                          |
| Protected Characteristic | No                                                                                                                           |
| Version                  | TBC                                                                                                                          |
| Approval Date            | TBC                                                                                                                          |
| Minimum                  | 01                                                                                                                           |
| Maximum                  | 35                                                                                                                           |
| Default                  |                                                                                                                              |
| Value Range              | Black   Fair  Grey  Mousey  White  Blue  Green  Orange  Purple  Yellow  Pink  Blonde  Brown  Dark Brown  Light Brown  Ginger |

[Image]

|            | Red  Auburn  Sandy  Multi  Other  None                 |
|------------|--------------------------------------------------------|
| Validation | 1. Alphanumeric                                        |
| Board      | NSAB                                                   |
| Owner      |                                                        |
|            | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward    |                                                        |
| Based On   | PND - PersonHairColourDyedColourList                   |

## 047: Person Relationship

| 047                      |                                                        |
|--------------------------|--------------------------------------------------------|
| POLE Class               | Person                                                 |
| Entity Group             | Person Description                                     |
| Attribute Name           | Person Relationship                                    |
| Attribute Description    | Relationship to Person                                 |
| Standard Type            | Police national to be agreed                           |
| Minimum Standard         | Yes                                                    |
| Protected Characteristic | Yes - Association exists with 'Sexual Orientation'     |
| Version                  | TBC                                                    |
| Approval Date            | TBC                                                    |
| Minimum                  | 01                                                     |
| Maximum                  | 35                                                     |
| Default                  |                                                        |
| Value Range              | See PND Database                                       |
| Validation               | 1. Alphanumeric                                        |
| Board                    | NSAB                                                   |
| Owner                    | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward                  |                                                        |
| Based On                 | PND - LinkedPersonRolePersonRelationshipReasonList     |

## 051: Telephone Type Code

| 051          | 051             |
|--------------|-----------------|
| POLE Class   | Object          |
| Entity Group | Virtual Address |

[Image]

| Attribute Name           | Telephone Type Code                                                                                                                                 |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Attribute Description    | Code denoting type of telephone number given                                                                                                        |
| Standard Type            | Police national to be agreed                                                                                                                        |
| Minimum Standard         | Yes                                                                                                                                                 |
| Protected Characteristic | No                                                                                                                                                  |
| Version                  | TBC                                                                                                                                                 |
| Approval Date            | TBC                                                                                                                                                 |
| Minimum                  | 04                                                                                                                                                  |
| Maximum                  | 04                                                                                                                                                  |
| Default                  |                                                                                                                                                     |
| Value Range              | LANH  Landline-Home  LANW  Landline-Work  MOBH  Mobile-Home  MOBW  Mobile-Work  FAXH  Fax-Home  FAXW - Fax-Work  PAGH  Pager-Home  PAGW  Pager-Work |
| Validation               | 1. Alphabetic                                                                                                                                       |
| Board                    | NSAB                                                                                                                                                |
| Owner                    | TBC                                                                                                                                                 |
| Steward                  |                                                                                                                                                     |
| Based On                 | CJS                                                                                                                                                 |

## 052: Telephone Country

| 052                      | 052                                                |
|--------------------------|----------------------------------------------------|
| POLE Class               | Object                                             |
| Entity Group             | Virtual Address                                    |
| Attribute Name           | Telephone Country                                  |
| Attribute Description    | Name of country assigned to telephone country code |
| Standard Type            | International                                      |
| Minimum Standard         | Yes                                                |
| Protected Characteristic | No                                                 |
| Version                  | TBC                                                |
| Approval Date            | TBC                                                |
| Minimum                  | 03                                                 |
| Maximum                  | 07                                                 |

[Image]

| Default     |                                                    |
|-------------|----------------------------------------------------|
| Value Range | ISO standards: E.123 and E.164                     |
| Validation  | 1. Alphanumeric  2. Valid country code on ISO list |
| Board       | International Telecommunication Union (ITU)        |
| Owner       | International Telecommunication Union (ITU)        |
| Steward     |                                                    |
| Based On    | ITU (E.123 and E.164)                              |

## 053: Telephone Number

| 053                      |                                                                                                                                         |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                  |
| Entity Group             | Virtual Address                                                                                                                         |
| Attribute Name           | Telephone Number                                                                                                                        |
| Attribute Description    | Telephone number including country code e.g. +441234567890 (note  no leading zero after country code and no spaces between  characters) |
| Standard Type            | International                                                                                                                           |
| Minimum Standard         | Yes                                                                                                                                     |
| Protected Characteristic | No                                                                                                                                      |
| Version                  | TBC                                                                                                                                     |
| Approval Date            | TBC                                                                                                                                     |
| Minimum                  | 11                                                                                                                                      |
| Maximum                  | 35                                                                                                                                      |
| Default                  |                                                                                                                                         |
| Value Range              | ISO standards: E.123 and E.164                                                                                                          |
| Validation               | 1. Alphanumeric ('+' required for international dialling code)  2. No spaces between characters                                         |
| Board                    | International Telecommunication Union (ITU)                                                                                             |
| Owner                    | International Telecommunication Union (ITU)                                                                                             |
| Steward                  |                                                                                                                                         |
| Based On                 | ITU (E.123 and E.164)                                                                                                                   |

## 054: Email Address

| 054          |                 |
|--------------|-----------------|
| POLE Class   | Object          |
| Entity Group | Virtual Address |

[Image]

| Attribute Name           | Email Address                                                                                           |
|--------------------------|---------------------------------------------------------------------------------------------------------|
| Attribute Description    | Electronic mail address                                                                                 |
| Standard Type            | Free text                                                                                               |
| Minimum Standard         | Yes                                                                                                     |
| Protected Characteristic | No                                                                                                      |
| Version                  | TBC                                                                                                     |
| Approval Date            | TBC                                                                                                     |
| Minimum                  | 05                                                                                                      |
| Maximum                  | 120                                                                                                     |
| Default                  |                                                                                                         |
| Value Range              |                                                                                                         |
| Validation               | 1. Alphanumeric and special characters  2. Must be of the form 'local-name@domain'  3. Must include '@' |
| Board                    | NSAB                                                                                                    |
| Owner                    | NPCC - IMORCC                                                                                           |
| Steward                  |                                                                                                         |
| Based On                 | IETF RFC5322 Section 3.4.1  (https://datatracker.ietf.org/doc/html/rfc5322)                             |

## 055: Social Media Tag

| 055                      | 055                                                                          |
|--------------------------|------------------------------------------------------------------------------|
| POLE Class               | Object                                                                       |
| Entity Group             | Virtual Address                                                              |
| Attribute Name           | Social Media Tag                                                             |
| Attribute Description    | A virtual identity usually relating to person or persons or an  organisation |
| Standard Type            | Free text                                                                    |
| Minimum Standard         | Yes                                                                          |
| Protected Characteristic | No                                                                           |
| Version                  | TBC                                                                          |
| Approval Date            | TBC                                                                          |
| Minimum                  | 01                                                                           |
| Maximum                  | 120                                                                          |
| Default                  |                                                                              |
| Value Range              |                                                                              |
| Validation               | 1. Alphanumeric                                                              |

[Image]

|                       | 2. Format should be 'Social Media Platform' - 'Tag'                                                                                                                                                                                                                                                                      |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board                 | NSAB                                                                                                                                                                                                                                                                                                                     |
| Owner                 | NPCC - IMORCC                                                                                                                                                                                                                                                                                                            |
| Steward               |                                                                                                                                                                                                                                                                                                                          |
| Based On              | None                                                                                                                                                                                                                                                                                                                     |
| Additional commentary | A person / organisation / persons can have multiple social media tags  (captured in Entity Description)  No specific standard is given and each social media platform may  have its own standard / format. Retained free text with format  guidance. Online identify may include URLs, web addresses, IP  addresses etc. |

## 056: UK Passport Number

| 056                      |                                                                                                                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                                                                              |
| Entity Group             | Identity                                                                                                                                                                            |
| Attribute Name           | UK Passport Number                                                                                                                                                                  |
| Attribute Description    | To identify a particular person by their UK passport number                                                                                                                         |
| Standard Type            | National                                                                                                                                                                            |
| Minimum Standard         | Yes                                                                                                                                                                                 |
| Protected Characteristic | No                                                                                                                                                                                  |
| Version                  | TBC                                                                                                                                                                                 |
| Approval Date            | TBC                                                                                                                                                                                 |
| Minimum                  | 07                                                                                                                                                                                  |
| Maximum                  | 09                                                                                                                                                                                  |
| Default                  |                                                                                                                                                                                     |
| Value Range              |                                                                                                                                                                                     |
| Validation               | 1. Two types only:  OLD:  - Must be 7 characters       - 1 alphabetic followed by 6 numeric      or      - 6 numeric followed by 1 alphabetic  NEW:  - Must be 9 numeric characters |
| Board                    | Her Majesty's Passport Office (HMPO)                                                                                                                                                |
| Owner                    | Her Majesty's Passport Office (HMPO)                                                                                                                                                |
| Steward                  |                                                                                                                                                                                     |

[Image]

## 057: Foreign Passport Number

| 057                      |                                                                                               |
|--------------------------|-----------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                        |
| Entity Group             | Identity                                                                                      |
| Attribute Name           | Foreign Passport Number                                                                       |
| Attribute Description    | To identify a particular person by their foreign passport number                              |
| Standard Type            | Free text                                                                                     |
| Minimum Standard         | Yes                                                                                           |
| Protected Characteristic | No                                                                                            |
| Version                  | TBC                                                                                           |
| Approval Date            | TBC                                                                                           |
| Minimum                  | 01                                                                                            |
| Maximum                  | 35                                                                                            |
| Default                  |                                                                                               |
| Value Range              |                                                                                               |
| Validation               | 1. Alphanumeric                                                                               |
| Board                    | NSAB                                                                                          |
| Owner                    | NPCC - IMORCC                                                                                 |
| Steward                  |                                                                                               |
| Based On                 |                                                                                               |
| Additional commentary    | This is free text to allow for multiple formats that may be used in  international countries. |

## 058: Passport Validity

| 058                      | 058                                                 |
|--------------------------|-----------------------------------------------------|
| POLE Class               | Person                                              |
| Entity Group             | Identity                                            |
| Attribute Name           | Passport Validity                                   |
| Attribute Description    | To identify whether a passport is in or out of date |
| Standard Type            | Free text                                           |
| Minimum Standard         | Yes                                                 |
| Protected Characteristic | No                                                  |
| Version                  | TBC                                                 |
| Approval Date            | TBC                                                 |
| Minimum                  | 02                                                  |

[Image]

| Maximum     | 03              |
|-------------|-----------------|
| Default     |                 |
| Value Range | Yes  No         |
| Validation  | 1. Alphanumeric |
| Board       | NSAB            |
| Owner       | NPCC - IMORCC   |
| Steward     |                 |
| Based On    |                 |

## 059: Passport Country

| 059                      |                                                                                                                                                                                                                                                                                                                                                    |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                                                                                                                                                                                                                                             |
| Entity Group             | Identity                                                                                                                                                                                                                                                                                                                                           |
| Attribute Name           | Passport Country                                                                                                                                                                                                                                                                                                                                   |
| Attribute Description    | To identify issued country of passport                                                                                                                                                                                                                                                                                                             |
| Standard Type            | International                                                                                                                                                                                                                                                                                                                                      |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                                                                |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                                                                 |
| Version                  | TBC                                                                                                                                                                                                                                                                                                                                                |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                                                                |
| Minimum                  | 03                                                                                                                                                                                                                                                                                                                                                 |
| Maximum                  | 03                                                                                                                                                                                                                                                                                                                                                 |
| Default                  |                                                                                                                                                                                                                                                                                                                                                    |
| Value Range              |                                                                                                                                                                                                                                                                                                                                                    |
| Validation               | 1. Alphabetic  2. 3 letter code must be on the ISO EN 3166 list                                                                                                                                                                                                                                                                                    |
| Board                    | ISO                                                                                                                                                                                                                                                                                                                                                |
| Owner                    | ISO BS EN3166                                                                                                                                                                                                                                                                                                                                      |
| Steward                  |                                                                                                                                                                                                                                                                                                                                                    |
| Based On                 | ISO BS EN 3166                                                                                                                                                                                                                                                                                                                                     |
| Additional commentary    | There is a standards countries list and ISO 3166-1 numeric codes are  three-digit country codes defined in ISO 3166-1. The 3 letter codes  are used for better visual association between codes and the country  names. 3 letter code would be assigned with an associated country  using a different data reference ISO BS EN 3166-2 and 3166-1-3 |

[Image]

## 060: National Insurance Number

| 060                      |                                                                                                                                                                                                                                                                                                                                                                     |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                                                                                                                                                                                                                                                                              |
| Entity Group             | Identity                                                                                                                                                                                                                                                                                                                                                            |
| Attribute Name           | National Insurance Number                                                                                                                                                                                                                                                                                                                                           |
| Attribute Description    | To identify a particular person by their National Insurance Number  (NINO)                                                                                                                                                                                                                                                                                          |
| Standard Type            | National                                                                                                                                                                                                                                                                                                                                                            |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                                                                                 |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                                                                                  |
| Version                  | TBC                                                                                                                                                                                                                                                                                                                                                                 |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                                                                                 |
| Minimum                  | 09                                                                                                                                                                                                                                                                                                                                                                  |
| Maximum                  | 09                                                                                                                                                                                                                                                                                                                                                                  |
| Default                  |                                                                                                                                                                                                                                                                                                                                                                     |
| Value Range              |                                                                                                                                                                                                                                                                                                                                                                     |
| Validation               | 1. Must be 9 characters  2. First 2 characters must be alphabetic  3. Next 6 characters must be numeric  4. Final character can be A, B, C, D or space  5. First character must not be D, F, I, Q, U or V  6. Second character must not be D, F, I, O, Q, U or V  7. First 2 characters must not be combinations of GB, NK, TN or ZZ (ie  neither GB nor BG etc...) |
| Board                    | Department of Work & Pensions (DWP)                                                                                                                                                                                                                                                                                                                                 |
| Owner                    | Department of Work & Pensions (DWP)                                                                                                                                                                                                                                                                                                                                 |
| Steward                  |                                                                                                                                                                                                                                                                                                                                                                     |
| Based On                 | Department of Work & Pensions (DWP)                                                                                                                                                                                                                                                                                                                                 |

## 061: UK Driving Licence Number

| 061                   | 061                                                    |
|-----------------------|--------------------------------------------------------|
| POLE Class            | Person                                                 |
| Entity Group          | Identity                                               |
| Attribute Name        | UK Driving Licence Number                              |
| Attribute Description | To identify a particular person by their driver number |
| Standard Type         | National                                               |
| Minimum Standard      | Yes                                                    |

[Image]

| Protected Characteristic   | No                                                                                                                                                                                                                                                                                                                                       |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Version                    | TBC                                                                                                                                                                                                                                                                                                                                      |
| Approval Date              | TBC                                                                                                                                                                                                                                                                                                                                      |
| Minimum                    | 16                                                                                                                                                                                                                                                                                                                                       |
| Maximum                    | 16                                                                                                                                                                                                                                                                                                                                       |
| Default                    |                                                                                                                                                                                                                                                                                                                                          |
| Value Range                |                                                                                                                                                                                                                                                                                                                                          |
| Validation                 | 1. Must be 16 characters  2. First 5 characters are alphanumeric  3. Next 6 characters must be numeric  4. Next 3 characters are alphanumeric  5. Last 2 characters are alphabetic  6. Second character of numeric section can only be 0, 1, 5 or 6  7. Fourth and fifth characters of numeric section must be in the range  of 01 to 31 |
| Board                      | Driver & Vehicle Licence Agency (DVLA)                                                                                                                                                                                                                                                                                                   |
| Owner                      | Driver & Vehicle Licence Agency (DVLA)                                                                                                                                                                                                                                                                                                   |
| Steward                    |                                                                                                                                                                                                                                                                                                                                          |
| Based On                   | Driver & Vehicle Licence Agency (DVLA)                                                                                                                                                                                                                                                                                                   |

## 062: Foreign Driving Licence Number

| 062                      |                                                                         |
|--------------------------|-------------------------------------------------------------------------|
| POLE Class               | Person                                                                  |
| Entity Group             | Identity                                                                |
| Attribute Name           | Foreign Driving Licence Number                                          |
| Attribute Description    | To identify a particular person by their foreign driving licence number |
| Standard Type            | Free text                                                               |
| Minimum Standard         | Yes                                                                     |
| Protected Characteristic | No                                                                      |
| Version                  | TBC                                                                     |
| Approval Date            | TBC                                                                     |
| Minimum                  | 01                                                                      |
| Maximum                  | 35                                                                      |
| Default                  |                                                                         |
| Value Range              |                                                                         |
| Validation               | 1. Alphanumeric                                                         |
| Board                    | NSAB                                                                    |

[Image]

| Owner                 | NPCC - IMORCC                                                                            |
|-----------------------|------------------------------------------------------------------------------------------|
| Steward               | Steward                                                                                  |
| Based On              | NPCC - IMORCC                                                                            |
| Additional commentary | This is free text to allow for multiple formats that may be used in  different countries |

## 063: Driving Licence Country

| 063                      |                                                                                                                                                                                                                                                                                                                                                    |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                                                                                                                                                                                                                             |
| Entity Group             | Identity                                                                                                                                                                                                                                                                                                                                           |
| Attribute Name           | Driving Licence Country                                                                                                                                                                                                                                                                                                                            |
| Attribute Description    | To identify country where driving licence was issued                                                                                                                                                                                                                                                                                               |
| Standard Type            | International                                                                                                                                                                                                                                                                                                                                      |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                                                                |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                                                                 |
| Version                  | TBC                                                                                                                                                                                                                                                                                                                                                |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                                                                |
| Minimum                  | 03                                                                                                                                                                                                                                                                                                                                                 |
| Maximum                  | 03                                                                                                                                                                                                                                                                                                                                                 |
| Default                  |                                                                                                                                                                                                                                                                                                                                                    |
| Value Range              |                                                                                                                                                                                                                                                                                                                                                    |
| Validation               | 1. Alphabetic  2. 3 Letter code  3. Code must be on the BS EN 3166 List                                                                                                                                                                                                                                                                            |
| Board                    | ISO                                                                                                                                                                                                                                                                                                                                                |
| Owner                    | ISO                                                                                                                                                                                                                                                                                                                                                |
| Steward                  |                                                                                                                                                                                                                                                                                                                                                    |
| Based On                 | ISO BS EN 3166                                                                                                                                                                                                                                                                                                                                     |
| Additional commentary    | There is a standards countries list and ISO 3166-1 numeric codes are  three-digit country codes defined in ISO 3166-1. The 3 letter codes  are used for better visual association between codes and the country  names. 3 letter code would be assigned with an associated country  using a different data reference ISO BS EN 3166-2 and 3166-1-3 |

## 065: Vehicle VRM

| 065        |        |
|------------|--------|
| POLE Class | Object |

[Image]

| Entity Group             | Vehicle                                                                                                                                                                                     |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attribute Name           | Vehicle VRM                                                                                                                                                                                 |
| Attribute Description    | Identifies the unique registration mark of a vehicle                                                                                                                                        |
| Standard Type            | National                                                                                                                                                                                    |
| Minimum Standard         | Yes                                                                                                                                                                                         |
| Protected Characteristic | No                                                                                                                                                                                          |
| Version                  | TBC                                                                                                                                                                                         |
| Approval Date            | TBC                                                                                                                                                                                         |
| Minimum                  | 01                                                                                                                                                                                          |
| Maximum                  | 11                                                                                                                                                                                          |
| Default                  | Free text                                                                                                                                                                                   |
| Value Range              | DVLA                                                                                                                                                                                        |
| Validation               | 1. Alphanumeric  2. No spaces are to be used                                                                                                                                                |
| Board                    | DVLA                                                                                                                                                                                        |
| Owner                    | DVLA                                                                                                                                                                                        |
| Steward                  |                                                                                                                                                                                             |
| Based On                 | DVLA                                                                                                                                                                                        |
| Additional commentary    | This is free text to allow for multiple formats that may be used in  different countries. This could be separated out to allow for UK  versus Foreign with DVLA validation available for UK |

## 066: Vehicle Make

| 066                      |                          |
|--------------------------|--------------------------|
| POLE Class               | Object                   |
| Entity Group             | Vehicle                  |
| Attribute Name           | Vehicle Make             |
| Attribute Description    | The brand of the vehicle |
| Standard Type            | National                 |
| Minimum Standard         | Yes                      |
| Protected Characteristic | No                       |
| Version                  | TBC                      |
| Approval Date            | TBC                      |
| Minimum                  | 01                       |
| Maximum                  | 35                       |
| Default                  |                          |
| Value Range              |                          |

[Image]

| Validation            | 1. Alphanumeric                                                                                                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board                 | DVLA                                                                                                                                                                                        |
| Owner                 | DVLA                                                                                                                                                                                        |
| Steward               |                                                                                                                                                                                             |
| Based On              | PND                                                                                                                                                                                         |
| Additional commentary | This is free text to allow for multiple formats that may be used in  different countries. This could be separated out to allow for UK  versus Foreign with DVLA validation available for UK |

## 067: Vehicle Model

| 067                      |                                                                                                                                                                                             |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                                                                      |
| Entity Group             | Vehicle                                                                                                                                                                                     |
| Attribute Name           | Vehicle Model                                                                                                                                                                               |
| Attribute Description    | The model of the vehicle                                                                                                                                                                    |
| Standard Type            | National                                                                                                                                                                                    |
| Minimum Standard         | Yes                                                                                                                                                                                         |
| Protected Characteristic | No                                                                                                                                                                                          |
| Version                  | TBC                                                                                                                                                                                         |
| Approval Date            | TBC                                                                                                                                                                                         |
| Minimum                  | 01                                                                                                                                                                                          |
| Maximum                  | 35                                                                                                                                                                                          |
| Default                  |                                                                                                                                                                                             |
| Value Range              |                                                                                                                                                                                             |
| Validation               | 1. Alphanumeric                                                                                                                                                                             |
| Board                    | DVLA                                                                                                                                                                                        |
| Owner                    | DVLA                                                                                                                                                                                        |
| Steward                  |                                                                                                                                                                                             |
| Based On                 | PND                                                                                                                                                                                         |
| Additional commentary    | This is free text to allow for multiple formats that may be used in  different countries. This could be separated out to allow for UK  versus Foreign with DVLA validation available for UK |

## 068: Vehicle Shape

| 068          |         |
|--------------|---------|
| POLE Class   | Object  |
| Entity Group | Vehicle |

[Image]

| Attribute Name           | Vehicle Shape                         |
|--------------------------|---------------------------------------|
| Attribute Description    | Vehicle Body / Shape                  |
| Standard Type            | National                              |
| Minimum Standard         | Yes                                   |
| Protected Characteristic | No                                    |
| Version                  | TBC                                   |
| Approval Date            | TBC                                   |
| Minimum                  | 01                                    |
| Maximum                  | 35                                    |
| Default                  |                                       |
| Value Range              |                                       |
| Validation               | 1. Alphanumeric                       |
| Board                    | DVLA                                  |
| Owner                    | DVLA                                  |
| Steward                  |                                       |
| Based On                 | PND - ConveryanceVehicleBodyShapeList |

## 069: Vehicle Colour

| 069                      |                       |
|--------------------------|-----------------------|
| POLE Class               | Object                |
| Entity Group             | Vehicle               |
| Attribute Name           | Vehicle Colour        |
| Attribute Description    | Colour of the vehicle |
| Standard Type            | National              |
| Minimum Standard         | Yes                   |
| Protected Characteristic | No                    |
| Version                  | TBC                   |
| Approval Date            | TBC                   |
| Minimum                  | 01                    |
| Maximum                  | 35                    |
| Default                  |                       |
| Value Range              |                       |
| Validation               | 1. Alphanumeric       |
| Board                    | DVLA                  |

[Image]

| Owner    | DVLA   |
|----------|--------|
| Steward  |        |
| Based On | N/A    |

## 070: Collar Number

| 070                      |                                                                                                              |
|--------------------------|--------------------------------------------------------------------------------------------------------------|
| POLE Class               | Person                                                                                                       |
| Entity Group             | Identity                                                                                                     |
| Attribute Name           | Collar Number                                                                                                |
| Attribute Description    | To identify a particular person when that person is a police worker  and has been allocated a collar number. |
| Standard Type            | Police national to be agreed                                                                                 |
| Minimum Standard         | Yes                                                                                                          |
| Protected Characteristic | No                                                                                                           |
| Version                  | TBC                                                                                                          |
| Approval Date            | TBC                                                                                                          |
| Minimum                  | 01                                                                                                           |
| Maximum                  | 10                                                                                                           |
| Default                  |                                                                                                              |
| Value Range              |                                                                                                              |
| Validation               | 1. Alphanumeric  2. Up to 10 characters                                                                      |
| Board                    | NSAB                                                                                                         |
| Owner                    | NPCC - WORKFORCE (People Management Portfolio)                                                               |
| Steward                  |                                                                                                              |
| Based On                 | NPCC                                                                                                         |

## 071: Criminal Records Office Number

| 071                      | 071                                                                      |
|--------------------------|--------------------------------------------------------------------------|
| POLE Class               | Object                                                                   |
| Entity Group             | Identity                                                                 |
| Attribute Name           | Criminal Records Office Number                                           |
| Attribute Description    | To identify a particular person by their Criminal Records Office  Number |
| Standard Type            | National                                                                 |
| Minimum Standard         | Yes                                                                      |
| Protected Characteristic | No                                                                       |

[Image]

| Version               | TBC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Approval Date         | TBC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Minimum               | 01                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Maximum               | 12                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Default               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Value Range           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Validation            | 1. Up to 12 characters  2.  Either: NNNNNN/YYD i.e. a 1 to 6 digit serial number (leading zero  suppressed) followed by an oblique, a two digit year part and a check  character OR   SF YY/NNNNNND i.e. the characters SF (no fingerprints held) followed  by a 2 digit year part (39 - 95 inclusive) an oblique a 1 to digit (leading  zero suppressed) serial number and a check character.   3. The numeric part of the CRO/SF number having been converted to  a single numeric value (YYNNNNNN for a full CRO Number YYNNNNN  for a post-64 SF Number and NNNNNN for a pre-65 SF Number (using  leading zeroes for serial part) and passed through the standard  Modulus 23 algorithm must generate a remainder value that matches  the given check character.   4. Check characters are A - Z excluding I O and S. |
| Board                 | ACRO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Owner                 | ACRO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Steward               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Based On              | PNC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Additional commentary | The unique number assigned by the National identification Services  (NIS) or from late 1988 by National Automated Fingerprint  Identification System (NAFIS) to identify the subject                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

## 072: Police National Computer ID

| 072                      | 072                                                                                                  |
|--------------------------|------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                               |
| Entity Group             | Identity                                                                                             |
| Attribute Name           | Police National Computer ID                                                                          |
| Attribute Description    | To identify a particular person by the number allocated by police  when creating a record on the PNC |
| Standard Type            | System Generated                                                                                     |
| Minimum Standard         | Yes                                                                                                  |
| Protected Characteristic | No                                                                                                   |

[Image]

| Version       | TBC                                                                                                                                                                                                                                                                                                                                                                                                              |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Approval Date | TBC                                                                                                                                                                                                                                                                                                                                                                                                              |
| Minimum       | 13                                                                                                                                                                                                                                                                                                                                                                                                               |
| Maximum       | 13                                                                                                                                                                                                                                                                                                                                                                                                               |
| Default       |                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Value Range   |                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Validation    | 1. 13 characters   2. Format: YYYY/NNNNNNND   3. A single value made of 2 digit year part and a fixed 7 digit serial  part, i.e. YYNNNNNNN, (leading zeroes used to expand serial part to 7  digits) is put through the Modulus 23 algorithm.   4. The derived value is divided by 23 and the modulus (remainder)  converted to a character i.e. 1 is A , 2 is B, 3 is C, .....to 0 is Z (ignoring  I, O and S). |
| Board         | NSAB                                                                                                                                                                                                                                                                                                                                                                                                             |
| Owner         | NPCC - IMORCC                                                                                                                                                                                                                                                                                                                                                                                                    |
| Steward       |                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Based On      | CJS                                                                                                                                                                                                                                                                                                                                                                                                              |

## 073: Arrest Summons Number

| 073                      | 073                                                                                                                                                              |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                                           |
| Entity Group             | Identity                                                                                                                                                         |
| Attribute Name           | Arrest Summons Number                                                                                                                                            |
| Attribute Description    | To identify a particular defendant by their arrest / summons number  (ASN), allocated by Police (or other prosecutor) when a defendant is  arrested or summonsed |
| Standard Type            | System Generated                                                                                                                                                 |
| Minimum Standard         | Yes                                                                                                                                                              |
| Protected Characteristic | No                                                                                                                                                               |
| Version                  | TBC                                                                                                                                                              |

[Image]

| Approval Date   | TBC                                                                                                                                                                                                                                |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Minimum         | 20                                                                                                                                                                                                                                 |
| Maximum         | 21                                                                                                                                                                                                                                 |
| Default         |                                                                                                                                                                                                                                    |
| Value Range     |                                                                                                                                                                                                                                    |
| Validation      | Format YYFFFFSSNNNNNNNNNNND  Where  YY  is a year indicator (as for PNC or CRO number)  FFFF  is a force/station identifier  SS  is a force system number  NNNNNNNNNNN  is a 1 - 11 digit number (for year)  is a check character" |
| Board           | NSAB                                                                                                                                                                                                                               |
| Owner           | NPCC - IMORCC                                                                                                                                                                                                                      |
| Steward         |                                                                                                                                                                                                                                    |
| Based On        | CJS                                                                                                                                                                                                                                |

## 074: Home Office Classification

| 074                      |                                                                                                                                                                                                                                           |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                                                                                                                    |
| Entity Group             | Incident                                                                                                                                                                                                                                  |
| Attribute Name           | Home Office Classification                                                                                                                                                                                                                |
| Attribute Description    | The Home Office Stats Code to which the offence belongs. The Home  Office Stats Code to which the offence belongs. This consists of two   elements separated by a '/'. This is required for Home Office  Management Information reporting |
| Standard Type            | National                                                                                                                                                                                                                                  |
| Minimum Standard         | Yes                                                                                                                                                                                                                                       |
| Protected Characteristic | No                                                                                                                                                                                                                                        |
| Version                  | TBC                                                                                                                                                                                                                                       |
| Approval Date            | TBC                                                                                                                                                                                                                                       |
| Minimum                  | 06                                                                                                                                                                                                                                        |
| Maximum                  | 06                                                                                                                                                                                                                                        |
| Default                  |                                                                                                                                                                                                                                           |
| Value Range              |                                                                                                                                                                                                                                           |
| Validation               | 1. Alphanumeric  2. Three numerics followed by '/' followed by two numerics (ie  NNN/NN)                                                                                                                                                  |

[Image]

| Board                 | Home Office                                                                                                                                         |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Owner                 | Home Office                                                                                                                                         |
| Steward               |                                                                                                                                                     |
| Based On              | Home Office                                                                                                                                         |
| Additional commentary | This consists of two elements separate by a '/'. This is required for  Home Office Management Information reporting  Linked to DS_80 (Offence Type) |

## 075: Verification of Death

| 075                      |                                                                                                                                                                 |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                                          |
| Entity Group             | Incident                                                                                                                                                        |
| Attribute Name           | Verification of Death                                                                                                                                           |
| Attribute Description    | Options for corroborating deaths                                                                                                                                |
| Standard Type            | Free text                                                                                                                                                       |
| Minimum Standard         | Yes                                                                                                                                                             |
| Protected Characteristic | No                                                                                                                                                              |
| Version                  | TBC                                                                                                                                                             |
| Approval Date            | TBC                                                                                                                                                             |
| Minimum                  | 01                                                                                                                                                              |
| Maximum                  | 35                                                                                                                                                              |
| Default                  |                                                                                                                                                                 |
| Value Range              | Details recorded as stated  Details used as currently held by force  Details used as currently held by PNC/PND  Death certificate produced  Unmapped Local Code |
| Board                    | NSAB                                                                                                                                                            |
| Validation               | 1. Alphanumeric                                                                                                                                                 |
| Owner                    | NPCC - IMORCC                                                                                                                                                   |
| Steward                  |                                                                                                                                                                 |
| Based On                 | PND - PersonDeathCorroborationStatusList                                                                                                                        |

## 076: Date of Death

| 076          | 076      |
|--------------|----------|
| POLE Class   | Object   |
| Entity Group | Incident |

[Image]

| Attribute Name           | Date of Death                                                                                                                                                                       |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attribute Description    | Date of Death                                                                                                                                                                       |
| Standard Type            | International                                                                                                                                                                       |
| Minimum Standard         | Yes                                                                                                                                                                                 |
| Protected Characteristic | No                                                                                                                                                                                  |
| Version                  | TBC                                                                                                                                                                                 |
| Approval Date            | TBC                                                                                                                                                                                 |
| Minimum                  | 01                                                                                                                                                                                  |
| Maximum                  | 10                                                                                                                                                                                  |
| Default                  |                                                                                                                                                                                     |
| Value Range              |                                                                                                                                                                                     |
| Validation               | 1. Numeric  2. Must be a valid date in the format DD-MM-YYYY  3. Leading zeros should be included  4. Must not be in the future  5. Must not be earlier than person's date of birth |
| Board                    | ISO                                                                                                                                                                                 |
| Owner                    | ISO                                                                                                                                                                                 |
| Steward                  |                                                                                                                                                                                     |
| Based On                 | ISO8601                                                                                                                                                                             |

## 078: Crime Type

| 078                   | 078                          |
|-----------------------|------------------------------|
| POLE Class            | Event                        |
| Entity Group          | Incident                     |
| Attribute Name        | Crime type                   |
| Attribute Description | Categorisation of crime type |
| Standard Type         | Police National to be agreed |
| Minimum Standard      | Yes                          |

[Image]

| Protected Characteristic   | No                                                                    |
|----------------------------|-----------------------------------------------------------------------|
| Version                    | TBC                                                                   |
| Approval Date              | TBC                                                                   |
| Minimum                    | 01                                                                    |
| Maximum                    | 35                                                                    |
| Default                    |                                                                       |
| Value Range                | See PND database                                                      |
| Validation                 | 1. Alphanumerics only                                                 |
| Board                      | NSAB                                                                  |
| Owner                      | NPCC - CRIME OPS (Performance and Standards portfolio)                |
| Steward                    |                                                                       |
| Based On                   | PND - OrganisedCrimeGroupCriminalityAssessmentAssessmentCrimeTypeList |

## 080: Offence Type (Offence Code)

| 080                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Event                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Entity Group             | Incident                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Attribute Name           | Offence Type (Offence Code)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Attribute Description    | Type of Offence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Standard Type            | Police national to be agreed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Version                  | TBC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Minimum                  | 07                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Maximum                  | 08                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Default                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Value Range              | See PND database                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Validation               | 1. Alphanumeric  AAYYNNN or COML NNN or XX00 NNN (all with an optional eighth  character (A) to qualify an Offence Code as an offence of either  attempting aiding and abetting, conspiring or inciting to commit an  offence). Note also that the quote marks are not part of the  validation but are used here to show literal content (e.g. MD71101  [Misuse of Drugs Act 1971 class B drug (cannabis)]) where:   AA is a code identifying an Act or other source (e.g. MD) YY is the year  of the Act etc (e.g. 71) |

[Image]

|          | NNN is a three digit number with leading zeroes as required  identifying an Offence   Reason within the Act etc. (e.g. 101) not necessarily inferring 101 or  more   offences within the act in the example given.  If the optional eighth character(A) is present then it must be one of  the four following codes:  A attempting  B aiding and abetting  C conspiring  I inciting  Or where:  COML is a literal to denote common laws followed by NNNA as  above.   Or where:   XX00 is a literal to denote an indictment rather than a charge  followed by NNNA as above.   |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board    | PNLD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Owner    | NPCC - CRIME OPS  (Performance and Standards portfolio)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Steward  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Based On | Police National Legal Database (PNLD)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

## 083: Crime Outcome

| 083                      | 083                                                                     |
|--------------------------|-------------------------------------------------------------------------|
| POLE Class               | Event                                                                   |
| Entity Group             | Incident                                                                |
| Attribute Name           | Crime Outcome                                                           |
| Attribute Description    | Range of resolved and unresolved outcomes based on CJS evidential  data |
| Standard Type            | Police National to be agreed                                            |
| Minimum Standard         | Yes                                                                     |
| Protected Characteristic | No                                                                      |
| Version                  | TBC                                                                     |
| Approval Date            | TBC                                                                     |
| Minimum                  | 01                                                                      |
| Maximum                  | 35                                                                      |
| Default                  |                                                                         |
| Value Range              | See PND Database (52 values)                                            |

[Image]

| Validation   | 1. Alphanumeric                                         |
|--------------|---------------------------------------------------------|
| Board        | NSAB                                                    |
| Owner        | NPCC - CRIME OPS  (Performance and Standards portfolio) |
| Steward      |                                                         |
| Based On     | PND                                                     |

## 084: Crime Status / Clear up Method

| 084                      |                                                         |
|--------------------------|---------------------------------------------------------|
| POLE Class               | Event                                                   |
| Entity Group             | Incident                                                |
| Attribute Name           | Crime Status / Clear Up Method                          |
| Attribute Description    | Outcome of Incident                                     |
| Standard Type            | Police National to be agreed                            |
| Minimum Standard         | Yes                                                     |
| Protected Characteristic | No                                                      |
| Version                  | TBC                                                     |
| Approval Date            | TBC                                                     |
| Minimum                  | 01                                                      |
| Maximum                  | 35                                                      |
| Default                  |                                                         |
| Value Range              | See PND Database (52 values)                            |
| Validation               | 1. Alphanumeric                                         |
| Board                    | NSAB                                                    |
| Owner                    | NPCC - CRIME OPS  (Performance and Standards portfolio) |
| Steward                  |                                                         |
| Based On                 | PND - PersonCrimeClearUpMethodList                      |

## 086: Arrest Reason

| 086                      | 086                                                                  |
|--------------------------|----------------------------------------------------------------------|
| POLE Class               | Event                                                                |
| Entity Group             | Incident                                                             |
| Attribute Name           | Arrest Reason                                                        |
| Attribute Description    | Selected list of Arrest Reasons used to define the reason for arrest |
| Standard Type            | Police National to be agreed                                         |
| Minimum Standard         | Yes                                                                  |
| Protected Characteristic | No                                                                   |
| Version                  | TBC                                                                  |

[Image]

| Approval Date   | TBC                                                     |
|-----------------|---------------------------------------------------------|
| Minimum         | 01                                                      |
| Maximum         | 120                                                     |
| Default         |                                                         |
| Value Range     | See PND Database (264 values)                           |
| Validation      | 1. Alphanumeric                                         |
| Board           | NSAB                                                    |
| Owner           | NPCC - CRIME OPS  (Performance and Standards portfolio) |
| Steward         |                                                         |
| Based On        | PND - ArrestDetentionReasonList                         |

## 088: MO (Modus Operandi)

| 088                      |                                                                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Event                                                                                                                                |
| Entity Group             | Incident                                                                                                                             |
| Attribute Name           | MO (Modus Operandi)                                                                                                                  |
| Attribute Description    | Description of entry, exit methods, means employed, instruments,  locations and victims and characters assumed.                      |
| Standard Type            | Police National to be agreed                                                                                                         |
| Minimum Standard         | Yes                                                                                                                                  |
| Protected Characteristic | No                                                                                                                                   |
| Version                  | TBC                                                                                                                                  |
| Approval Date            | TBC                                                                                                                                  |
| Minimum                  | 20                                                                                                                                   |
| Maximum                  | 300                                                                                                                                  |
| Default                  |                                                                                                                                      |
| Value Range              |                                                                                                                                      |
| Validation               | 1. Alphanumeric  2. Minimum of 20 characters                                                                                         |
| Board                    | NSAB                                                                                                                                 |
| Owner                    | NPCC - CRIME OPS  (Performance and Standards portfolio)                                                                              |
| Steward                  |                                                                                                                                      |
| Based On                 | PND                                                                                                                                  |
| Additional commentary    | We have retained free text at present. CLMS_Context_PND_v5_7  provides 3 layers of classification which may be a preferred approach. |

## 091: NSIR Opening Code

[Image]

| 091                      |                                                        |
|--------------------------|--------------------------------------------------------|
| POLE Class               | Object                                                 |
| Entity Group             | Incident                                               |
| Attribute Name           | NSIR Opening Code                                      |
| Attribute Description    | National Standard for Incident Reporting Opening code. |
| Standard Type            | Police National to be agreed                           |
| Minimum Standard         | Yes                                                    |
| Protected Characteristic | No                                                     |
| Version                  | TBC                                                    |
| Approval Date            | TBC                                                    |
| Minimum                  | 03                                                     |
| Maximum                  | 03                                                     |
| Default                  |                                                        |
| Value Range              |                                                        |
| Validation               | 1. Numeric                                             |
| Board                    | NSAB                                                   |
| Owner                    | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward                  |                                                        |
| Based On                 | NISR 2011                                              |

## 092: NSIR Closing Code

| 092                      |                                                       |
|--------------------------|-------------------------------------------------------|
| POLE Class               | Object                                                |
| Entity Group             | Incident                                              |
| Attribute Name           | NSIR Closing Code                                     |
| Attribute Description    | National Standard for Incident Reporting Closing code |
| Standard Type            | Police National to be agreed                          |
| Minimum Standard         | Yes                                                   |
| Protected Characteristic | No                                                    |
| Version                  | TBC                                                   |
| Approval Date            | TBC                                                   |
| Minimum                  | 03                                                    |
| Maximum                  | 03                                                    |
| Default                  |                                                       |
| Value Range              |                                                       |
| Validation               | 1. Numeric                                            |
| Board                    | NSAB                                                  |

[Image]

| Owner    | NPCC - CRIME OPS (Performance and Standards portfolio)   |
|----------|----------------------------------------------------------|
| Steward  | NISR 2011                                                |
| Based On | NISR 2011                                                |

## 093: Repeat Victim

| 093                      |                                                 |
|--------------------------|-------------------------------------------------|
| POLE Class               | Person                                          |
| Entity Group             | Incident                                        |
| Attribute Name           | Repeat Victim                                   |
| Attribute Description    | Whether the person has been a victim previously |
| Standard Type            | Free text                                       |
| Minimum Standard         | Yes                                             |
| Protected Characteristic | No                                              |
| Version                  | TBC                                             |
| Approval Date            | TBC                                             |
| Minimum                  | 02                                              |
| Maximum                  | 03                                              |
| Default                  |                                                 |
| Value Range              | Yes  No                                         |
| Validation               | 1. Alphanumeric                                 |
| Board                    | NSAB                                            |
| Owner                    | NPCC - IMORCC                                   |
| Steward                  |                                                 |
| Based On                 |                                                 |

## 094: Repeat Offender

| 094                      | 094                                                |
|--------------------------|----------------------------------------------------|
| POLE Class               | Person                                             |
| Entity Group             | Incident                                           |
| Attribute Name           | Repeat Offender                                    |
| Attribute Description    | Whether the person has been an offender previously |
| Standard Type            | Free text                                          |
| Minimum Standard         | Yes                                                |
| Protected Characteristic | No                                                 |
| Version                  | TBC                                                |
| Approval Date            | TBC                                                |

[Image]

| Minimum     | 02              |
|-------------|-----------------|
| Maximum     | 03              |
| Default     |                 |
| Value Range | Yes  No         |
| Validation  | 1. Alphanumeric |
| Board       | NSAB            |
| Owner       | NPCC - IMORCC   |
| Steward     |                 |
| Based On    |                 |

## 095: Children Present

| 095                      |                                   |
|--------------------------|-----------------------------------|
| POLE Class               | Object                            |
| Entity Group             | Incident                          |
| Attribute Name           | Children Present                  |
| Attribute Description    | Were children present at the time |
| Standard Type            | Free text                         |
| Minimum Standard         | Yes                               |
| Protected Characteristic | No                                |
| Version                  | TBC                               |
| Approval Date            | TBC                               |
| Minimum                  | 02                                |
| Maximum                  | 03                                |
| Default                  |                                   |
| Value Range              | Yes  No                           |
| Validation               | 1. Alphanumeric                   |
| Board                    | NSAB                              |
| Owner                    | NPCC - IMORCC                     |
| Steward                  |                                   |
| Based On                 |                                   |

## 096: Hate Crime

| 096          |          |
|--------------|----------|
| POLE Class   | Object   |
| Entity Group | Incident |

[Image]

| Attribute Name           | Hate Crime                                                                                                                                                                                                                                               |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attribute Description    | What type of Hate Crime - allowing for other non-monitored strands                                                                                                                                                                                       |
| Standard Type            | Police national to be agreed                                                                                                                                                                                                                             |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                      |
| Protected Characteristic | Association exists with 'Sexual Orientation' and 'Race'                                                                                                                                                                                                  |
| Version                  | TBC                                                                                                                                                                                                                                                      |
| Approval Date            | TBC                                                                                                                                                                                                                                                      |
| Minimum                  | 03                                                                                                                                                                                                                                                       |
| Maximum                  | 25                                                                                                                                                                                                                                                       |
| Default                  |                                                                                                                                                                                                                                                          |
| Value Range              | N/A  Race  Religion  Sexual Orientation  Transgender  Other                                                                                                                                                                                              |
| Validation               | 1. Alphanumeric                                                                                                                                                                                                                                          |
| Board                    | NSAB                                                                                                                                                                                                                                                     |
| Owner                    | NPCC - DIVERSITY, EQUALITY & INCLUSION (Hate Crime Portfolio)                                                                                                                                                                                            |
| Steward                  |                                                                                                                                                                                                                                                          |
| Based On                 | College of Policing Guidance                                                                                                                                                                                                                             |
| Additional commentary    | This lists '5 monitored strands of Hate Crime'. Hate crime requires  motivation by a hostility or prejudice based on one of these strands.  There is also allowance for 'non-monitored' strands as well. These are  not covered as the minimum standard. |

## 097: Property - Category

| 097                      |                                           |
|--------------------------|-------------------------------------------|
| POLE Class               | Object                                    |
| Entity Group             | Property                                  |
| Attribute Name           | Property - Category                       |
| Attribute Description    | Categorisation of property defined by PND |
| Standard Type            | Police national to be agreed              |
| Minimum Standard         | Yes                                       |
| Protected Characteristic |                                           |
| Version                  | TBC                                       |
| Approval Date            | TBC                                       |
| Minimum                  | 01                                        |
| Maximum                  | 35                                        |

[Image]

| Default     |                                                           |
|-------------|-----------------------------------------------------------|
| Value Range | Drawn from PND (59 Items)                                 |
| Validation  | 1. Alphanumeric  2. One option only to be drawn from list |
| Board       | NSAB                                                      |
| Owner       | NPCC - CRIME OPS (Performance and Standards portfolio)    |
| Steward     |                                                           |
| Based On    | PND - ObjectCategoryList                                  |

## 098: Property - Description

| 098                      |                                                        |
|--------------------------|--------------------------------------------------------|
| POLE Class               | Object                                                 |
| Entity Group             | Property                                               |
| Attribute Name           | Property - Description                                 |
| Attribute Description    | A short description of the property                    |
| Standard Type            | Free text                                              |
| Minimum Standard         | Yes                                                    |
| Protected Characteristic | No                                                     |
| Version                  | TBC                                                    |
| Approval Date            | TBC                                                    |
| Minimum                  | 01                                                     |
| Maximum                  | 120                                                    |
| Default                  |                                                        |
| Value Range              |                                                        |
| Validation               | 1. Alphanumeric                                        |
| Board                    | NSAB                                                   |
| Owner                    | NPCC - CRIME OPS (Performance and Standards portfolio) |
| Steward                  |                                                        |
| Based On                 |                                                        |

## 099: Unique ID Number Type

| 099                   | 099                          |
|-----------------------|------------------------------|
| POLE Class            | Object                       |
| Entity Group          | Property                     |
| Attribute Name        | Unique ID number type        |
| Attribute Description | Type of Identity Number      |
| Standard Type         | Police national to be agreed |

[Image]

| Minimum Standard         | Yes                                                   |
|--------------------------|-------------------------------------------------------|
| Protected Characteristic | No                                                    |
| Version                  | TBC                                                   |
| Approval Date            | TBC                                                   |
| Minimum                  | 01                                                    |
| Maximum                  | 35                                                    |
| Default                  |                                                       |
| Value Range              |                                                       |
| Validation               | 1. Alphanumeric                                       |
| Board                    | NSAB                                                  |
| Owner                    | NPCC -CRIME OPS (Performance and Standards portfolio) |
| Steward                  |                                                       |
| Based On                 | PND - ObjectIdentityNumberList                        |

## 100: Unique Number

| 100                      |                                                          |
|--------------------------|----------------------------------------------------------|
| POLE Class               | Object                                                   |
| Entity Group             | Property                                                 |
| Attribute Name           | Unique number                                            |
| Attribute Description    | ID or Serial number for the property under consideration |
| Standard Type            | Free text                                                |
| Minimum Standard         | Yes                                                      |
| Protected Characteristic | No                                                       |
| Version                  | TBC                                                      |
| Approval Date            | TBC                                                      |
| Minimum                  | 01                                                       |
| Maximum                  | 35                                                       |
| Default                  |                                                          |
| Value Range              |                                                          |
| Validation               | 1. Alphanumeric                                          |
| Board                    | NSAB                                                     |
| Owner                    | NPCC -CRIME OPS (Performance and Standards portfolio)    |
| Steward                  |                                                          |
| Based On                 |                                                          |

## 101: Photograph Description

## 101

[Image]

| POLE Class               | Object                                                |
|--------------------------|-------------------------------------------------------|
| Entity Group             | Property                                              |
| Attribute Name           | Photograph description                                |
| Attribute Description    | Description of the photograph                         |
| Standard Type            | Free text                                             |
| Minimum Standard         | Yes                                                   |
| Protected Characteristic | No                                                    |
| Version                  | TBC                                                   |
| Approval Date            | TBC                                                   |
| Minimum                  | 01                                                    |
| Maximum                  | 120                                                   |
| Default                  |                                                       |
| Value Range              |                                                       |
| Validation               | 1. Alphanumeric                                       |
| Board                    | NSAB                                                  |
| Owner                    | NPCC -CRIME OPS (Performance and Standards portfolio) |
| Based on                 |                                                       |

## 102: Photograph

| 102                      |                                                                    |
|--------------------------|--------------------------------------------------------------------|
| POLE Class               | Object                                                             |
| Entity Group             | Property                                                           |
| Attribute Name           | Photograph                                                         |
| Attribute Description    | Photograph of person                                               |
| Standard Type            | Image                                                              |
| Minimum Standard         | Yes                                                                |
| Protected Characteristic | Yes - Association might exist with some protective characteristics |
| Version                  | TBC                                                                |
| Approval Date            | TBC                                                                |
| Minimum                  | N/A                                                                |
| Maximum                  | N/A                                                                |
| Default                  |                                                                    |
| Value Range              |                                                                    |
| Validation               | 1. Alphanumeric                                                    |
| Board                    |                                                                    |
| Owner                    |                                                                    |
| Based on                 |                                                                    |

[Image]

## 103: Date of Photograph

| 103                      |                                                                                                                                   |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                            |
| Entity Group             | Property                                                                                                                          |
| Attribute Name           | Date of Photograph                                                                                                                |
| Attribute Description    | Photograph of person                                                                                                              |
| Standard Type            | International                                                                                                                     |
| Minimum Standard         | Yes                                                                                                                               |
| Protected Characteristic | No                                                                                                                                |
| Version                  | TBC                                                                                                                               |
| Approval Date            | TBC                                                                                                                               |
| Minimum                  | 01                                                                                                                                |
| Maximum                  | 10                                                                                                                                |
| Default                  |                                                                                                                                   |
| Value Range              | Numeric                                                                                                                           |
| Validation               | 1. Numeric  2. Must be a valid date in the format DD-MM-YYYY  3. Leading zeros should be included  4. Should not be in the future |
| Board                    | ISO                                                                                                                               |
| Owner                    | ISO                                                                                                                               |
| Based On                 | ISO8601                                                                                                                           |

## 105: Stop Nature

| 105                      | 105                                    |
|--------------------------|----------------------------------------|
| POLE Class               | Event                                  |
| Entity Group             | Incident                               |
| Attribute Name           | Stop Nature                            |
| Attribute Description    | Code A of PACE Act 1984 classification |
| Standard Type            | Police national to be agreed           |
| Minimum Standard         | Yes                                    |
| Protected Characteristic | Yes                                    |
| Version                  | TBC                                    |
| Approval Date            | TBC                                    |
| Minimum                  | 01                                     |
| Maximum                  | 35                                     |

[Image]

| Default     |                                                                                                                                                                                                                                    |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Value Range | Agreed Stop Nature list                                                                                                                                                                                                            |
| Validation  | 1. Alphanumeric                                                                                                                                                                                                                    |
| Board       | NSAB                                                                                                                                                                                                                               |
| Owner       | NPCC - OPERATIONS (Stop and Search Portfolio)                                                                                                                                                                                      |
| Based On    | College of Policing Guidance (CODE A   Revised   Code of Practice for the exercise by:   Police Officers of Statutory   Powers of stop and search   Police Officers and Police Staff of requirements to record public  encounters) |

## 106: ASB Class

| 106                      |                                                                                                               |
|--------------------------|---------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                        |
| Entity Group             | Incident                                                                                                      |
| Attribute Name           | ASB Class                                                                                                     |
| Attribute Description    | Category of Anti-social Behaviour                                                                             |
| Standard Type            | Police national to be agreed                                                                                  |
| Minimum Standard         | Yes                                                                                                           |
| Protected Characteristic | No                                                                                                            |
| Version                  | TBC                                                                                                           |
| Approval Date            | TBC                                                                                                           |
| Minimum                  | 01                                                                                                            |
| Maximum                  | 35                                                                                                            |
| Default                  |                                                                                                               |
| Value Range              | Personal  Nuisance  Environmental                                                                             |
| Validation               | 1. Alphanumeric                                                                                               |
| Board                    | NSAB                                                                                                          |
| Owner                    | NPCC - LOCAL POLICING (Anti-Social Behaviour & Arson portfolio)                                               |
| Based On                 | NSIR 2011 (The National Standard for Incident Recording)  (incorporating the National Incident Category List) |

## 107: ASB Type

[Image]

| 107                      |                                                                                                                                                                                                                                                                                                        |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POLE Class               | Object                                                                                                                                                                                                                                                                                                 |
| Entity Group             | Incident                                                                                                                                                                                                                                                                                               |
| Attribute Name           | ASB Type                                                                                                                                                                                                                                                                                               |
| Attribute Description    | Type of Anti-social behaviour                                                                                                                                                                                                                                                                          |
| Standard Type            | Police national to be agreed                                                                                                                                                                                                                                                                           |
| Minimum Standard         | Yes                                                                                                                                                                                                                                                                                                    |
| Protected Characteristic | No                                                                                                                                                                                                                                                                                                     |
| Version                  | TBC                                                                                                                                                                                                                                                                                                    |
| Approval Date            | TBC                                                                                                                                                                                                                                                                                                    |
| Minimum                  | 01                                                                                                                                                                                                                                                                                                     |
| Maximum                  | 35                                                                                                                                                                                                                                                                                                     |
| Default                  |                                                                                                                                                                                                                                                                                                        |
| Value Range              | Vehicle abandoned  Vehicle nuisance or inappropriate use  Rowdy or inconsiderate behaviour  Rowdy or nuisance neighbours  Littering or drugs paraphernalia  Animal problems  Trespassing  Nuisance calls  Street drinking  Prostitution-related activity  Nuisance noise  Begging  Misuse of fireworks |
| Validation               | 1. Alphanumeric                                                                                                                                                                                                                                                                                        |
| Board                    | NSAB                                                                                                                                                                                                                                                                                                   |
| Owner                    | NPCC - LOCAL POLICING (Anti-Social Behaviour & Arson portfolio)                                                                                                                                                                                                                                        |
| Based On                 | Metropolitan guidance                                                                                                                                                                                                                                                                                  |

## 108: ASB Questionnaire

| 108                   | 108                                                                       |
|-----------------------|---------------------------------------------------------------------------|
| POLE Class            | Object                                                                    |
| Entity Group          | Incident                                                                  |
| Attribute Name        | ASB Questionnaire                                                         |
| Attribute Description | Whether or not an Anti-social Behaviour questionnaire has been  completed |

[Image]

| Standard Type            | Free text                                                       |
|--------------------------|-----------------------------------------------------------------|
| Minimum Standard         | Yes                                                             |
| Protected Characteristic | No                                                              |
| Version                  | TBC                                                             |
| Approval Date            | TBC                                                             |
| Minimum                  | 02                                                              |
| Maximum                  | 03                                                              |
| Default                  |                                                                 |
| Value Range              | Yes  No                                                         |
| Validation               | 1. Alphanumeric                                                 |
| Board                    | NSAB                                                            |
| Owner                    | NPCC - LOCAL POLICING (Anti-Social Behaviour & Arson portfolio) |
| Based On                 |                                                                 |

## 109: Telephone Extension

| 109                      |                                                 |
|--------------------------|-------------------------------------------------|
| POLE Class               | Object                                          |
| Entity Group             | Object                                          |
| Attribute Name           | Telephone extension                             |
| Attribute Description    | Extension number to a telephone number exchange |
| Standard Type            | Free text                                       |
| Minimum Standard         | Yes                                             |
| Protected Characteristic | No                                              |
| Version                  | TBC                                             |
| Approval Date            | TBC                                             |
| Minimum                  | 01                                              |
| Maximum                  | 06                                              |
| Default                  |                                                 |
| Value Range              |                                                 |
| Validation               | 1. Numeric                                      |
| Board                    | NSAB                                            |
| Owner                    | NPCC - IMORCC                                   |
| Based On                 |                                                 |

## 110: Correct Checks

## 110

[Image]

| POLE Class               | Event                                                                                  |
|--------------------------|----------------------------------------------------------------------------------------|
| Entity Group             | Object                                                                                 |
| Attribute Name           | Correct Checks                                                                         |
| Attribute Description    | Confirmation that the correct checks have been undertaken in the  case of a Hate Crime |
| Standard Type            | Free text                                                                              |
| Minimum Standard         | Yes                                                                                    |
| Protected Characteristic | No                                                                                     |
| Version                  | TBC                                                                                    |
| Approval Date            | TBC                                                                                    |
| Minimum                  | 01                                                                                     |
| Maximum                  | 120                                                                                    |
| Default                  |                                                                                        |
| Value Range              | Yes  No                                                                                |
| Validation               | 1. Alphanumeric                                                                        |
| Board                    | NSAB                                                                                   |
| Owner                    | NPCC - DIVERSITY, EQUALITY & INCLUSION (Hate Crime Portfolio)                          |
| Based On                 |                                                                                        |

## 111: SAFE Number

| 111                      |                                                                |
|--------------------------|----------------------------------------------------------------|
| POLE Class               | Object                                                         |
| Entity Group             | Object                                                         |
| Attribute Name           | SAFE number                                                    |
| Attribute Description    | Safe contact number of relative/person to contact              |
| Standard Type            | International                                                  |
| Minimum Standard         | Yes                                                            |
| Protected Characteristic | No                                                             |
| Version                  | TBC                                                            |
| Approval Date            | TBC                                                            |
| Minimum                  | 11                                                             |
| Maximum                  | 35                                                             |
| Default                  |                                                                |
| Value Range              | Yes  No                                                        |
| Validation               | 1. Alphanumeric ('+' required for international dialling code) |

[Image]

|                       | 2. No spaces between characters                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Board                 | CJS                                                                                                                                                                                                                     |
| Owner                 | NPCC - DIVERSITY, EQUALITY & INCLUSION (Hate Crime Portfolio)                                                                                                                                                           |
| Based On              | CJS                                                                                                                                                                                                                     |
| Additional commentary | The complete telephone number should always be used.  STD codes no longer have a geographic significance.  Data elements elsewhere in the Data Standards will refer to this entry  for details on length and validation |

[Image]

[Image]

## 7. References

-  Anti-social Behaviour, Crime and Policing Act 2014 - Anti-social Behaviour, Crime and Policing Act 2014 (legislation.gov.uk)
-  APP College of Policing (CoP) -Stop and search (college.police.uk) - The police have a range of statutory powers of stop and search available to them, depending on the circumstances. Most, but not all, of these powers require an officer to have reasonable grounds for suspicion that an unlawful item is being carried
-  APP College of Policing (CoP) - the professional body for the police in England and Wales. It was established in 2012 to take over a number of training and development roles that were the responsibility of the National Policing Improvement Agency. Missing Person entity class - Missing persons (college.police.uk)
-  Association of Chief Police Officers (ACPO) - was a not-for-profit private limited company that for many years led the development of policing practices in England, Wales and Northern Ireland. Now superseded by the National Police Chiefs' Council. Safeguarding and Investigating the Abuse of Vulnerable Adult information Microsoft Word - VA Mature Draft v9.doc (college.police.uk)
-  Code of Practice for Victims of Crime - introduced in 2006, setting out the minimum levels of service which victims can expect from agencies that are signatories to it.
-  Code of Practice for the Law Enforcement Data Service (LEDS) - This Code provides a framework and operational context for relevant authorities, such as Her Majesty's Inspectorate of Constabulary and Fire &amp; Rescue Services (HMICFRS) to monitor how LEDS is governed, managed and used.
-  Crime and Disorder Act (1998) - Crime and Disorder Act 1998 (legislation.gov.uk)
-  Driver and Vehicle Licensing Agency (DVLA) - maintains a database of drivers in Great Britain and a database of vehicles for the entire United Kingdom.
-  Department for Work and Pensions (DWP) - government department responsible for welfare and pension policy.
-  Law Enforcement Capability Model - a framework for Law Enforcement that is developed collaboratively with Forces and other Law Enforcement bodies.  The model has 3 levels - Strategy, Business capabilities and business processes and Services that support business processes.
-  Management of Police Information (MoPI) - a section of the APP on information management which was developed to support the Code of Practice for Management of Police Information 2005 and is being updated to align with the revised the Code of Practice on Information and Records Management. Provides guidance designed to contribute to enhanced public safety by improving the ability of the police service to properly manage and share operational information within a nationally consistent framework.
-  National Crime Agency (NCA) - A national law enforcement agency in the United Kingdom. It is the UK's lead agency against organised crime; human, weapon and drug trafficking; cybercrime; and economic crime that goes across regional and international borders. NCA Guidance on reporting routes relating to vulnerable persons -Microsoft Word - Vulnerable Person Reporting Routes Nov 2016 v0.3 (nationalcrimeagency.gov.uk)

[Image]

-  Witness Definition -What is WITNESS? definition of WITNESS (Black's Law Dictionary) (thelawdictionary.org)
-  Safeguarding Vulnerable Groups Act 2006 - Safeguarding Vulnerable Groups Act 2006 (legislation.gov.uk)
-  https://www.police.uk/pu/contact-the-police/what-and-how-to-report/what-report/
-  Police and Criminal Evidence Act 1984 (PACE ) NPIA LPG1.7.04. PACE Code D (publishing.service.gov.uk)