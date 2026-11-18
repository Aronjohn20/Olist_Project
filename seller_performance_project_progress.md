# Seller Performance & Marketplace Operations Analytics Platform

## Project Progress Journal --- From Problem Discovery to Data Architecture

**Purpose:** This document records the work completed so far, the
situations considered, the decisions made, and why those decisions were
taken. It distinguishes decisions already made from proposals that still
need validation.

------------------------------------------------------------------------

# 1. Project overview

The project is a **Seller Performance & Marketplace Operations Analytics
Platform** using the public Olist Brazilian E-Commerce dataset.

The aim is to build a production-style analytics engineering solution
that centralizes marketplace data and helps business users understand
seller performance. The goal is not merely to create a dashboard. The
project should demonstrate business understanding, data architecture,
ingestion, transformation, data quality, analysis, reporting, testing,
documentation, and deployment.

**Scope limitation:** Olist is historical public data. We do not have
access to Olist's internal live systems or actual managers. The project
can be production-style and may simulate scheduled data arrivals, but it
must not claim to be a live production system used by Olist.

# 2. Phase 0 --- Problem discovery

## Situation identified

A marketplace may have many sellers and information spread across
different datasets: orders, order items, products, sellers, payments,
reviews, and delivery timestamps.

A manager who wants to understand a seller's performance may have to
combine multiple reports manually. Looking at one dataset or revenue
alone does not provide a complete picture. A seller could generate high
revenue while having poor reviews or delivery performance.

## Business problem framed

> Marketplace managers lack a centralized and consistent analytical view
> of seller performance. Information is scattered across multiple
> datasets, making it difficult to compare sellers, identify sellers
> that need attention, investigate performance patterns, and prioritize
> operational follow-up.

This framing was important because the project started with a business
problem rather than choosing a technology or dashboard first.

## Objectives decided

### Objective 1 --- Centralized data management

Bring scattered marketplace datasets into a centralized data
environment.

**Why:** This reduces repeated manual data combination, makes sources
queryable together, and allows consistent transformations and business
definitions to be reused.

### Objective 2 --- Seller performance analysis and decision support

Help users identify strong-performing sellers, sellers who may need
attention, changes in seller performance, and patterns worth
investigating.

**Why:** The business needs to know more than how much a seller sells.
Sales, customer experience, and delivery performance can provide
different views of performance.

The platform is intended to support investigation, not to claim that a
metric proves the cause of a problem. For example, a high late-delivery
rate is a signal to investigate; it does not automatically prove that
the seller caused the delay.

# 3. Users and their needs

Two user groups were identified.

## Marketplace Manager

Needs an overall view of marketplace and seller performance.

Questions include: - Which sellers perform well? - Which sellers need
attention? - How do sellers compare? - Is a seller improving or
declining? - Which sellers should be prioritized for investigation?

The manager's role is to monitor, compare, identify, and prioritize.

## Seller Operations Team

Needs to investigate sellers who have been identified as needing
attention.

Questions include: - Which performance indicators are weak? - Are poor
reviews appearing alongside delivery problems? - Are issues concentrated
in particular product categories? - What patterns should be
investigated? - What operational follow-up may be appropriate?

The manager identifies where attention may be needed; the operations
team investigates what may be happening.

# 4. Phase 1 --- Requirements gathering

Requirements gathering was started to understand what users need before
deciding how to build the system. The questions and sample answers
discussed are initial working requirements, not verified statements from
actual Olist stakeholders.

## Business questions identified

-   Which sellers perform well?
-   Which sellers need attention?
-   How do sellers compare?
-   Is seller performance improving or declining over time?
-   Are poor reviews associated with delivery problems?
-   Are performance patterns different across product categories?
-   Which sellers should be investigated first?

## Candidate performance areas and measures

  -----------------------------------------------------------------------
  Area                                Candidate measures / analysis
  ----------------------------------- -----------------------------------
  Sales                               Revenue, order count, items sold,
                                      average order value

  Customer experience                 Average review score, percentage of
                                      poor reviews

  Delivery                            Average delivery time,
                                      late-delivery rate

  Product / category                  Seller performance across
                                      categories

  Trends                              Monthly or historical performance
                                      changes
  -----------------------------------------------------------------------

These are candidate measures. Their exact business definitions and
calculation rules are not finalized yet.

## Granularity and filters

The intended analysis should support: - Marketplace level - Product
category level - Seller level

Candidate filters: - Date - Seller - Product category - Seller
location - Performance level

## Data quality and success criteria

An important requirement was that incorrect or incomplete data should
not silently appear as reliable information. The pipeline should
validate data and make relevant problems visible.

The intended success is that a manager can identify sellers needing
attention and understand the indicators behind that decision without
manually combining multiple reports. Success is not simply "a dashboard
has been built."

## Refresh frequency caveat

Daily refresh was discussed as an illustrative requirement. However,
Olist is a historical public snapshot, not a live operational feed. A
scheduled refresh cannot create genuinely new Olist transactions. Any
simulated batch arrivals must be disclosed as simulation.

# 5. Dataset selection and understanding

## Dataset selected

The project uses the **Olist Brazilian E-Commerce Public Dataset**. It
contains historical e-commerce information about orders, items,
customers, sellers, products, payments, reviews, and related data.

## Source files identified

1.  `olist_customers_dataset.csv`
2.  `olist_orders_dataset.csv`
3.  `olist_order_items_dataset.csv`
4.  `olist_products_dataset.csv`
5.  `olist_sellers_dataset.csv`
6.  `olist_order_payments_dataset.csv`
7.  `olist_order_reviews_dataset.csv`
8.  `olist_geolocation_dataset.csv`
9.  `product_category_name_translation.csv`
10. `olist_marketing_qualified_leads_dataset.csv`
11. `olist_closed_deals_dataset.csv`

The user noted that some source names written in the proposed model were
not exact CSV filenames. The list above records the dataset filenames
discussed.

## Why grain matters

The files do not all represent the same kind of row. An orders file may
have one row per order, while order items and payments may have multiple
rows per order. Reviews also need to be checked rather than assumed to
be one-to-one with orders.

Joining tables without understanding their grain can duplicate records
and inflate calculations.

**Example of join fan-out:** If one order has 3 item rows and 2 payment
rows, joining the two many-side tables directly on `order_id` can
produce 3 × 2 = 6 rows. Item values and payment values can then be
duplicated in aggregations.

This is why grain, keys, and cardinality must be understood before
creating analytical models.

## Dataset limitations considered

The public dataset is not a complete live marketplace environment. It
does not provide every operational data source a real marketplace might
have, such as a complete live feed, full inventory history, detailed
shipment-event history, or every possible profit, returns, and
customer-support measure. The project must not invent unavailable
information.

# 6. Initial technology stack

The stack was discussed as a proposed implementation. Some
infrastructure choices were deliberately left open.

  -----------------------------------------------------------------------
  Area                    Technology              Intended responsibility
  ----------------------- ----------------------- -----------------------
  Programming             Python                  Repeatable ingestion
                                                  and automation

  Database                PostgreSQL              Centralized raw and
                                                  transformed storage

  Query language          SQL                     Querying and
                                                  transformations

  Transformation          dbt                     Organizing, testing,
                                                  and documenting SQL
                                                  models

  Data modelling          Dimensional modelling   Business-oriented
                                                  analytical structures

  Data quality            dbt tests + SQL /       Validating data and
                          Python                  business rules

  Visualization           Power BI                Interactive reporting

  Version control         Git + GitHub            Tracking project
                                                  changes

  Development environment Antigravity / VS Code   Writing and managing
                                                  code

  API integration         Python + REST APIs, if  External sources when
                          justified               needed

  Orchestration           To be decided           Coordinating pipeline
                                                  execution

  Containerization        Docker, if justified    Reproducible execution

  CI/CD                   GitHub Actions planned  Automated checks and
                                                  workflows

  Hosting / deployment    To be decided           Running outside the
                                                  local environment

  Documentation           Markdown + dbt docs     Explaining setup,
                                                  models, and system
                                                  behaviour
  -----------------------------------------------------------------------

### Why Python for ingestion?

Manual imports could load the CSV files, but Python makes ingestion
repeatable and maintainable. It can later support consistent loading,
logging, error handling, duplicate handling, and automated execution.

### Why PostgreSQL?

PostgreSQL provides a relational database in which source data can be
stored centrally and queried using SQL. It is a reasonable choice for
this dataset and for demonstrating database and analytics engineering
skills.

### Why dbt?

dbt organizes SQL transformations into manageable, testable, and
documented models. It does not replace PostgreSQL: PostgreSQL stores the
data; dbt runs and manages transformations against it.

The planned layers are: - **Staging:** standardize and clean source
data. - **Intermediate:** combine and enrich data using reusable
logic. - **Marts:** create business-ready models for analysis and
reporting.

### Decisions postponed

Orchestration, hosting, Docker, deployment details, and the exact CI/CD
workflow have not been finalized. The intention is to introduce tools
when requirements justify them, not simply to make the architecture look
complex.

# 7. Phase 2 --- Product and system design

The purpose of this phase was to decide, at a high level, how the system
would work and how data would move through it. This is a logical system
design, not yet a detailed database schema or deployment architecture.

## Main flow decided

1.  Olist CSV files act as the source data.
2.  Python reads and ingests the files.
3.  PostgreSQL stores the original data in a RAW layer.
4.  dbt transforms the data through STAGING, INTERMEDIATE, and MARTS.
5.  SQL business analysis uses the prepared data.
6.  Power BI presents the analysis.
7.  Marketplace Managers and the Seller Operations Team use the
    dashboard.

## Why separate the layers?

### RAW

Preserves the ingested source data in a centralized database. This
supports traceability and allows downstream models to be rebuilt when
transformation logic changes.

### STAGING

Makes source data consistent and easier to use. Typical work includes
renaming columns, standardizing formats, casting data types, and basic
cleaning.

### INTERMEDIATE

Contains reusable transformation logic. It can combine or enrich staging
models without making every business mart repeat the same joins.

### MARTS

Contains business-ready models designed to support seller performance
analysis, comparisons, trends, and operational investigation.

## Where business analytics fits

Business analytics does not need to be a separate software system.
Reusable business logic can live in dbt models, particularly in the
marts layer. SQL analysis and Power BI can consume those prepared
models. The important requirement is consistent, reusable business
definitions.

## Supporting engineering processes

The design also identified data quality and testing,
scheduling/orchestration, logging/monitoring, GitHub version control and
CI/CD, documentation, and appropriate security/access management. These
support the pipeline but do not all need to be implemented immediately.

## Initial logical architecture

``` mermaid
flowchart TD
    A["Olist CSV Data Sources"] --> B["Python Ingestion"]
    B --> C[("PostgreSQL - RAW")]
    C --> D["dbt - STAGING"]
    D --> E["dbt - INTERMEDIATE"]
    E --> F["dbt - MARTS"]
    F --> G["SQL Business Analytics"]
    G --> H["Power BI Dashboard"]
    H --> I["Marketplace Manager"]
    H --> J["Seller Operations Team"]

    K["Data Quality & Testing"] -.-> B
    K -.-> D
    K -.-> E
    K -.-> F
    L["Scheduling / Orchestration"] -.-> B
    L -.-> D
    M["GitHub - Version Control & CI/CD"] -.-> B
    M -.-> D
    M -.-> H
```

Solid arrows show the main data flow. Dotted arrows represent supporting
engineering practices. This is conceptual; exact tools and deployment
details remain to be finalized.

## Phase 2 outcome

The high-level system flow and responsibilities were established. The
next question became how the data itself should be structured so the
system can answer the business questions correctly. That led to Phase 3.

# 8. Phase 3 --- Data architecture

The first part of this phase was to understand the source datasets and
decide their grain, keys, and relationships before creating database
tables or transformation models.

The work focuses on: 1. What each dataset represents. 2. What one row
represents (grain). 3. Which columns identify records (primary or
composite keys). 4. Which columns connect datasets (foreign keys). 5.
Relationship cardinality (one-to-one, one-to-many, etc.). 6. How to join
tables without duplicating data. 7. How to organize data for seller
performance analysis.

## 8.1 User's proposed central fact tables

### `fct_order_items`

**Source:** Olist order-items dataset.

**Columns listed:** - `order_id` - `order_item_id` - `product_id` -
`seller_id` - `price` - `freight_value`

**Intended grain:** One row per order item, identified by the
combination of `order_id` and `order_item_id`.

**Why:** This table connects each item sold to its product and seller
and contains item-level price and freight information. It is a useful
foundation for item and seller sales analysis.

### `fct_order_payments`

**Source:** Olist order-payments dataset.

**Columns listed:** - `order_id` - `payment_sequential` -
`payment_type` - `payment_installments` - `payment_value`

**Intended grain:** One row per payment record, identified by `order_id`
and `payment_sequential`.

**Why:** An order can have multiple payment records. Payments have a
different grain from order items, so they should not be treated as one
payment value per item.

### Why two fact tables were proposed

Order items and payments describe different business events and have
different grains. Keeping them separate reduces the risk of join fan-out
and incorrect aggregations.

## 8.2 Other proposed tables

  ------------------------------------------------------------------------------------
  Proposed model name                  Source / subject        Intended role in the
                                                               proposal
  ------------------------------------ ----------------------- -----------------------
  `dim_customers`                      Customers               Customer information

  `dim_orders`                         Orders                  Order information and
                                                               timestamps

  `dim_order_reviews`                  Order reviews           Review score and review
                                                               information

  `dim_products`                       Products                Product attributes

  `dim_product_category_translation`   Product category        Portuguese-to-English
                                       translation             category mapping

  `dim_sellers`                        Sellers                 Seller information and
                                                               location

  `dim_b2b_closed_deals`               Closed deals            Seller acquisition /
                                                               B2B deal information
  ------------------------------------------------------------------------------------

These are the names and roles in the user's proposal. Their final
fact/dimension classification still needs review.

## 8.3 Relationships proposed

  -------------------------------------------------------------------------------
  One side          Many / optional   Join key                  Proposed
                    side                                        cardinality
  ----------------- ----------------- ------------------------- -----------------
  Products          Order items       `product_id`              1 to many

  Sellers           Order items       `seller_id`               1 to many

  Orders            Order items       `order_id`                1 to many

  Orders            Order payments    `order_id`                1 to many

  Customers         Orders            `customer_id`             1 to 1

  Orders            Order reviews     `order_id`                1 to 0 or 1

  Product category  Products          `product_category_name`   1 to many
  translation                                                   

  Sellers           B2B closed deals  `seller_id`               1 to 0 or 1
  -------------------------------------------------------------------------------

These are proposed relationships. They must be checked against the
actual source data before being treated as guaranteed cardinalities.

## 8.4 Why the relationships were proposed

-   **Products → order items:** connects each sold item to product
    attributes such as category, weight, and dimensions. This enables
    category-level analysis.
-   **Sellers → order items:** identifies which seller supplied each
    item. This is essential for seller-level sales analysis.
-   **Orders → order items:** connects item-level records to order-level
    information such as purchase timestamps, status, and delivery dates.
-   **Orders → order payments:** connects payment records to the
    corresponding order. Keeping payments separate from items avoids
    multiplying item and payment rows in a direct many-to-many join.
-   **Customers → orders:** connects an order to its customer record,
    enabling customer and geographic analysis.
-   **Orders → reviews:** connects orders to customer feedback. Review
    scores can support customer-experience analysis, but the proposed
    zero-or-one relationship needs validation.
-   **Category translation → products:** maps Portuguese category names
    to English labels for reporting.
-   **Sellers → B2B closed deals:** connects sellers to
    acquisition/onboarding context such as business segment, declared
    revenue, or sales representative, if those fields and matching IDs
    are available.

# 9. Mentor review --- points to investigate

The following are review recommendations, not decisions that the user
has already adopted.

## 9.1 Should `dim_orders` be a fact table?

The proposed order table contains transactional information such as
order status and timestamps. One option is to model it as `fct_orders`,
with one row per order.

An order represents a business event with a lifecycle. Its dates and
status can support measures such as order volume, processing time, and
delivery performance. The final classification should follow the
analytical model, not simply the source filename.

## 9.2 Should `dim_order_reviews` be a fact table?

Reviews represent feedback events and contain information such as review
score and timestamps. One option is `fct_order_reviews`.

Before deciding, inspect whether `order_id` is unique in the source. Do
not assume one review per order without checking.

## 9.3 Customer identifiers

Olist has both `customer_id` and `customer_unique_id`.

-   `customer_id` identifies the customer record associated with an
    order.
-   `customer_unique_id` can identify the same customer across multiple
    orders.

If the analysis needs returning-customer behaviour, `customer_unique_id`
is important. The model should preserve this distinction.

## 9.4 Validate closed-deals cardinality

The proposed seller-to-closed-deals relationship is one-to-zero-or-one
only if the data supports it. Check whether `seller_id` is unique in the
closed-deals source, whether seller IDs match, and whether multiple deal
records can exist for a seller.

## 9.5 Do not classify tables by renaming source files

A source table does not automatically become a dimension or fact because
of its filename or subject. Classification depends on the business
event/entity, grain, measures, descriptive context, and analytical use.

# 10. Progress tracker

  -----------------------------------------------------------------------
  Area                                Status
  ----------------------------------- -----------------------------------
  Business problem                    Initial framing completed

  Main business objectives            Identified

  User groups                         Identified

  Initial business questions          Identified

  Candidate performance areas / KPIs  Identified; definitions pending

  Dataset selected                    Completed

  Source CSV inventory                Identified

  Initial technology stack            Proposed

  High-level system design            Completed

  Main data flow                      Established

  Initial fact tables                 Proposed

  Initial dimensions / supporting     Proposed
  tables                              

  Grain and key decisions             User reports having worked these
                                      out; detailed validation still
                                      required

  Relationships and cardinalities     Proposed; source-data validation
                                      pending

  Final dimensional model             Not finalized

  PostgreSQL schemas and tables       Not yet designed/finalized

  Python ingestion                    Not yet covered in this design
                                      progress

  dbt transformations                 Not yet implemented

  Final KPI definitions               Not finalized

  Power BI dashboard                  Not yet implemented

  Deployment and orchestration        Deliberately postponed
  -----------------------------------------------------------------------

# 11. Immediate next step

The next task is to finalize the **logical analytical data model**.

The question raised in the review is:

> For analysing seller performance across revenue, number of orders,
> items sold, delivery performance, and customer satisfaction, what
> should be the central analytical fact table?

Options to evaluate:

1.  Use `fct_order_items` as the main fact for item-level seller
    analysis, while bringing other measures in at their correct grains.
2.  Create a separate seller-level aggregated fact table for reporting.
3.  Use another model or a combination of these approaches.

This decision has not yet been made.

It must be based on the business questions and the grain of each
measure. Revenue, payment, delivery, and review measures must not be
combined in a way that duplicates values.

After that: 1. Finalize the logical model. 2. Validate keys,
relationships, and cardinalities against the CSV files. 3. Decide the
initial PostgreSQL table structure. 4. Move to ingestion design and
implementation.

# 12. Lessons from the work so far

-   **Start with the business problem, not the dashboard.** The
    dashboard is a delivery mechanism; the business decision is the
    reason for building the system.
-   **Understand users and their decisions.** The manager and operations
    team have related but different responsibilities.
-   **Understand grain before joining data.** Grain determines how
    records can be joined and aggregated safely.
-   **Different business events may need separate fact tables.** Order
    items and payments have different grains.
-   **Validate relationships against the data.** A relationship that
    seems logical must still be checked for uniqueness and matching
    keys.
-   **Do not add tools without a reason.** Orchestration, Docker, cloud
    hosting, and other infrastructure should be introduced when
    justified.
-   **Signals are not causes.** A poor delivery rate or review score can
    point to a pattern, but investigation is needed before attributing
    responsibility.

------------------------------------------------------------------------

## Overall summary

The project has moved from understanding a marketplace
seller-performance problem to gathering initial requirements, selecting
a dataset and technology direction, designing a high-level system, and
proposing the first analytical tables and relationships.

The main remaining work in the current design stage is to validate the
proposed relationships and finalize the analytical data model.
Implementation of ingestion, dbt transformations, KPI logic, dashboards,
and deployment comes afterward.
