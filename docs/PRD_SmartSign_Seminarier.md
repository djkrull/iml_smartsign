# Product Requirements Document: SmartSign Seminar Display System

**Product Name:** SmartSign Seminar Display
**Version:** 1.0
**Date:** 2025-11-17
**Author:** Institut Mittag-Leffler IT Team
**Status:** Approved

---

## 1. Executive Summary

The SmartSign Seminar Display System automatically displays upcoming seminars on digital screens at Institut Mittag-Leffler (IML). The system filters seminar data from a master Excel export to show only relevant, current-week seminars tagged for public display, eliminating the need for manual updates.

**Key Benefits:**
- Eliminates manual weekly updates to digital signage
- Ensures displayed information is always current and accurate
- Reduces administrative overhead for seminar communications
- Improves visitor experience with up-to-date seminar information

---

## 2. Problem Statement

### Current Situation
Institut Mittag-Leffler hosts numerous seminars throughout each academic term (semester), with data exported from a centralized system. The organization needs to display upcoming seminars on digital screens, but faces these challenges:

1. **Data Volume:** Master export contains entire semester's worth of seminars (175+ events)
2. **Manual Updates:** Staff must manually filter and update display content weekly
3. **Timing:** Past seminars must be removed promptly to avoid confusion
4. **Selective Display:** Only seminars tagged for public display ("website") should appear
5. **Automation:** System must be self-sustaining without daily intervention

### Impact
- Staff time wasted on repetitive manual updates
- Risk of displaying outdated or incorrect information
- Inconsistent seminar promotion across the institute

---

## 3. Goals and Objectives

### Primary Goals
1. **Automate** the filtering and display of seminar information
2. **Display** only relevant, current-week seminars on digital screens
3. **Eliminate** manual intervention for routine updates
4. **Ensure** information accuracy and timeliness

### Success Metrics
- Zero manual updates required for routine seminar display
- 100% accuracy in displayed seminar times and details
- No past seminars displayed on screens
- System updates automatically within 24 hours of data changes

---

## 4. User Personas

### Primary Users

**Persona 1: Visitors and Researchers**
- **Need:** Quickly see what seminars are happening this week
- **Expectation:** Accurate, up-to-date information displayed on lobby screens
- **Pain Point:** Confusion when displayed information is outdated or incorrect

**Persona 2: Administrative Staff**
- **Need:** Minimize time spent updating digital signage
- **Expectation:** Automatic updates without manual intervention
- **Pain Point:** Repetitive weekly tasks of filtering and publishing seminar lists

**Persona 3: Seminar Organizers**
- **Need:** Confidence that their seminars are properly promoted
- **Expectation:** Seminars tagged "website" appear automatically on displays
- **Pain Point:** Uncertainty about whether promotion is working

---

## 5. Functional Requirements

### 5.1 Data Filtering Requirements

| Req ID | Requirement | Priority | Acceptance Criteria |
|--------|-------------|----------|-------------------|
| FR-1 | System shall filter seminars to current week only (Monday-Friday) | Critical | Only seminars between Monday 00:00 and Friday 23:59 of current week are included |
| FR-2 | System shall exclude past seminars | Critical | No seminars with start time before current time are displayed |
| FR-3 | System shall filter by "website" tag | Critical | Only seminars with "website" in Tag(s) column are included |
| FR-4 | System shall extract speaker information from HTML descriptions | High | Speaker name and institution extracted from `<b>Speaker</b>` HTML pattern |
| FR-5 | System shall format time for display | High | Time displayed as "HH:MM-HH:MM" format (e.g., "09:30-10:30") |
| FR-6 | System shall clean seminar titles | Medium | Prefixes like "WS," removed from titles |
| FR-7 | System shall format dates in readable format | High | Dates displayed as "Weekday DD Mon" (e.g., "Tuesday 18 Nov") |

### 5.2 Data Output Requirements

| Req ID | Requirement | Priority | Acceptance Criteria |
|--------|-------------|----------|-------------------|
| FR-8 | System shall generate CSV file with standardized columns | Critical | Output CSV contains: Title, Speaker, Date_Formatted, Time, Location |
| FR-9 | System shall use UTF-8 encoding with BOM | High | CSV file readable in Excel and SmartSign without encoding issues |
| FR-10 | System shall handle empty data gracefully | Medium | Empty CSV created if no seminars match filter criteria |

### 5.3 Automation Requirements

| Req ID | Requirement | Priority | Acceptance Criteria |
|--------|-------------|----------|-------------------|
| FR-11 | System shall run automatically daily | Critical | Script executes at 00:00 every day via Windows Task Scheduler |
| FR-12 | System shall publish CSV to web server | Critical | Generated CSV automatically deployed to accessible web URL |
| FR-13 | SmartSign shall fetch updated data automatically | Critical | SmartSign CMS retrieves CSV from web server on schedule |

### 5.4 Display Requirements

| Req ID | Requirement | Priority | Acceptance Criteria |
|--------|-------------|----------|-------------------|
| FR-14 | Display shall show seminar title | Critical | Full seminar title visible and readable |
| FR-15 | Display shall show speaker name and institution | Critical | Speaker information clearly presented |
| FR-16 | Display shall show date in readable format | Critical | Date shown as weekday and date (e.g., "Tuesday 18 Nov") |
| FR-17 | Display shall show time range | Critical | Time shown as start-end range (e.g., "09:30-10:30") |
| FR-18 | Display shall show location/room | High | Room location displayed for each seminar |
| FR-19 | Display shall NOT show abstracts or descriptions | Medium | Only title, speaker, date, time, location shown |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Req ID | Requirement | Target |
|--------|-------------|--------|
| NFR-1 | Script execution time | < 30 seconds for 200 seminars |
| NFR-2 | CSV file size | < 50 KB for typical weekly data |
| NFR-3 | Web server response time | < 2 seconds for CSV download |

### 6.2 Reliability

| Req ID | Requirement | Target |
|--------|-------------|--------|
| NFR-4 | System uptime | 99.5% (excluding scheduled maintenance) |
| NFR-5 | Error handling | Script continues even if individual seminar data is malformed |
| NFR-6 | Data accuracy | 100% accuracy for correctly formatted source data |

### 6.3 Maintainability

| Req ID | Requirement | Target |
|--------|-------------|--------|
| NFR-7 | Code documentation | All functions documented with docstrings |
| NFR-8 | Error messages | Clear Swedish error messages for operational staff |
| NFR-9 | Logging | Script outputs detailed execution log to console |

### 6.4 Usability

| Req ID | Requirement | Target |
|--------|-------------|--------|
| NFR-10 | Setup time | < 2 hours for new installation by IT staff |
| NFR-11 | Configuration | All paths and settings in clearly marked variables |
| NFR-12 | Troubleshooting | Clear preview of filtered data in console output |

---

## 7. Data Requirements

### 7.1 Input Data

**Source:** Excel file exported from seminar management system
**Location:** `C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx`
**Update Frequency:** Manual export as needed (typically weekly or per-term)

**Required Columns:**
- `Id` - Unique identifier
- `Start date` - Seminar start date (datetime)
- `Start time` - Start time (timedelta format: "0 days HH:MM:SS")
- `End time` - End time (timedelta format)
- `Title` - Seminar title (may include prefix like "WS,")
- `Description` - HTML description containing speaker information
- `Tag(s)` - Tags including "website" for public display
- `Room location` - Room/venue name

### 7.2 Output Data

**Format:** CSV (UTF-8 with BOM)
**Location:** `C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv`
**Deployment:** Uploaded to web server for SmartSign access

**Output Columns:**
- `Title_Original` - Original title (for reference)
- `Title` - Cleaned title (prefixes removed)
- `Speaker` - Speaker name and institution
- `Date` - ISO date format (for sorting)
- `Date_Formatted` - Human-readable date ("Tuesday 18 Nov")
- `Time` - Formatted time range ("09:30-10:30")
- `Location` - Room/venue name

---

## 8. User Stories

### Story 1: Visitor Viewing Seminars
**As a** visiting researcher
**I want to** see this week's upcoming seminars on the lobby screen
**So that** I can plan which talks to attend

**Acceptance Criteria:**
- Only current week's seminars are shown
- Past seminars are not displayed
- Seminar times are accurate and clearly formatted
- Display updates automatically each day

### Story 2: Administrative Staff Setup
**As an** IT administrator
**I want to** set up the seminar display system once
**So that** it runs automatically without my intervention

**Acceptance Criteria:**
- Setup can be completed in under 2 hours
- Clear documentation guides installation
- System runs automatically via Task Scheduler
- Error notifications are clear and actionable

### Story 3: Seminar Organizer Tagging
**As a** seminar program coordinator
**I want to** control which seminars appear on public displays
**So that** only appropriate seminars are promoted publicly

**Acceptance Criteria:**
- Seminars tagged with "website" appear automatically
- Seminars without tag do not appear
- Tagging is done in the source system (Excel export)
- Changes reflect within 24 hours

---

## 9. System Dependencies

### Required Software
- **Python 3.8+** with pandas and openpyxl libraries
- **Windows 10/11** with Task Scheduler
- **SmartSign CMS** version 11.x
- **Web server** with HTTPS support (for CSV hosting)

### External Systems
- **Seminar Management System** (produces ProgramExport.xlsx)
- **SmartSign CMS** (displays content)
- **Digital Screens** (hardware for display)

---

## 10. Constraints and Assumptions

### Constraints
- System runs on Windows environment only
- Source data format (Excel) is fixed and cannot be changed
- SmartSign CMS limitations apply to template design
- Weekly cycle runs Monday-Friday only (no weekend seminars)

### Assumptions
- Source Excel file is updated manually by program coordinator
- Web server has adequate uptime and bandwidth
- SmartSign CMS is configured and operational
- Network connectivity is stable between all components
- "website" tag is applied consistently in source data

---

## 11. Future Enhancements

### Phase 2 Potential Features
1. **Email Notifications:** Alert staff if no seminars found for current week
2. **Multi-Week Display:** Option to show next week's seminars
3. **Multiple Tags:** Support filtering by multiple tag criteria
4. **API Integration:** Direct integration with seminar management system
5. **Real-time Updates:** Hourly updates instead of daily
6. **Multi-Language:** Support for Swedish/English bilingual display
7. **Calendar Integration:** Sync with IML calendar systems
8. **Mobile App:** Mobile view of current week's seminars

---

## 12. Success Criteria

The product will be considered successful when:

1. **Zero manual updates** required for weekly seminar display
2. **100% automation** of filtering and publishing process
3. **Staff time savings** of 2-3 hours per week
4. **No user complaints** about outdated or incorrect seminar information
5. **System uptime** of >99% over first 3 months
6. **Positive feedback** from both staff and visitors

---

## 13. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | IML IT Team | [Approved] | 2025-11-17 |
| Technical Lead | IML IT Team | [Approved] | 2025-11-17 |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-17 | IML IT Team | Initial version |
