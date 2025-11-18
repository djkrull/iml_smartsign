# Architecture Decision Record: SmartSign Seminar Display System

**Project:** SmartSign Seminar Display
**Date:** 2025-11-17
**Status:** Approved
**Decision Makers:** IML IT Team

---

## Table of Contents

1. [ADR-001: Use Web-Based CSV Hosting](#adr-001-use-web-based-csv-hosting)
2. [ADR-002: Python for Data Processing](#adr-002-python-for-data-processing)
3. [ADR-003: CSV as Data Exchange Format](#adr-003-csv-as-data-exchange-format)
4. [ADR-004: Weekly Filtering Strategy](#adr-004-weekly-filtering-strategy)
5. [ADR-005: Daily Batch Processing](#adr-005-daily-batch-processing)
6. [ADR-006: Windows Task Scheduler for Automation](#adr-006-windows-task-scheduler-for-automation)
7. [ADR-007: Regex for Speaker Extraction](#adr-007-regex-for-speaker-extraction)
8. [ADR-008: Tag-Based Content Filtering](#adr-008-tag-based-content-filtering)

---

## ADR-001: Use Web-Based CSV Hosting

### Context
SmartSign CSV datasources can fetch data through multiple methods:
- Local file access via SmartSign Sync
- Direct HTTP/HTTPS URL fetching
- Fetching through SmartSign server proxy

The filtered seminar data needs to be accessible to SmartSign CMS reliably and automatically.

### Decision
**Host the CSV file on a web server and provide SmartSign with an HTTPS URL.**

### Rationale

**Why web-based hosting:**
1. **Better Documentation:** SmartSign documentation explicitly describes URL-based CSV fetching
2. **Reliability:** Web servers provide consistent uptime and access
3. **Infrastructure Availability:** IML already has web server infrastructure
4. **Simplicity:** No dependency on SmartSign Sync local installation
5. **Accessibility:** URL can be accessed from any location, not tied to specific machine
6. **Standard Protocol:** HTTPS is a standard, well-understood protocol
7. **Caching:** Web servers can leverage HTTP caching mechanisms

**Why NOT SmartSign Sync:**
- Limited documentation on how it serves local files
- Requires SmartSign Sync to be running continuously
- Tied to specific local machine
- More complex troubleshooting
- Unknown failure modes

**Why NOT manual upload:**
- Defeats automation goal
- Introduces human error
- Time-consuming
- Not sustainable

### Consequences

**Positive:**
- Robust, well-documented solution
- Easy to verify (just visit the URL)
- Standard web infrastructure
- Can leverage web server monitoring
- Easy to troubleshoot
- Scales well if more screens added

**Negative:**
- Requires web server access and configuration
- Additional deployment step (local file → web server)
- Network dependency (requires internet connectivity)
- Potential security consideration (CSV must be publicly accessible)

**Mitigation:**
- Use automated deployment (FTP, rsync, or CI/CD)
- CSV data is public information (no security risk)
- Web server has high uptime SLA

### Alternatives Considered
1. **SmartSign Sync local files** - Rejected due to limited documentation
2. **SmartSign Media Library upload** - Rejected due to manual process
3. **Direct database connection** - Rejected due to complexity and security

---

## ADR-002: Python for Data Processing

### Context
Need to process Excel data, apply complex filtering logic, extract data from HTML, and generate CSV output. Multiple language options available: Python, JavaScript/Node.js, PowerShell, Bash.

### Decision
**Use Python 3.8+ with pandas library for data processing.**

### Rationale

**Why Python:**
1. **Pandas Library:** Industry-standard for data manipulation and Excel processing
2. **Excel Support:** Native Excel reading via openpyxl integration
3. **Data Processing:** Excellent for filtering, transforming, and cleaning data
4. **Regex Support:** Built-in regex for HTML parsing
5. **Cross-Platform:** Code works on Windows, Linux, macOS
6. **Readability:** Clear, maintainable code
7. **Ecosystem:** Rich library ecosystem for future enhancements
8. **Team Expertise:** Python widely known by IT staff

**Why NOT JavaScript/Node.js:**
- Requires npm dependencies
- More boilerplate for data processing
- Less natural for Excel/CSV manipulation

**Why NOT PowerShell:**
- Windows-only
- Limited data processing libraries
- Less familiar to general IT staff

**Why NOT Bash:**
- Poor structured data handling
- Requires external tools (awk, sed)
- Error-prone for complex parsing

### Consequences

**Positive:**
- Fast development time
- Robust data processing
- Easy to maintain and extend
- Good error handling
- Clear code structure
- Wide community support

**Negative:**
- Requires Python installation
- Dependency on pandas and openpyxl packages
- Slightly larger footprint than native scripting

**Mitigation:**
- Python commonly available on Windows systems
- Dependencies installed via pip (simple one-time setup)
- Virtual environment can isolate dependencies

---

## ADR-003: CSV as Data Exchange Format

### Context
SmartSign supports multiple datasource types: CSV, JSON, XML, SQL databases. Need to choose format for data exchange between filtering script and SmartSign CMS.

### Decision
**Use CSV (Comma-Separated Values) with UTF-8 encoding and BOM.**

### Rationale

**Why CSV:**
1. **SmartSign Native Support:** CSV Datasource is well-documented SmartSign feature
2. **Simplicity:** Simple format, easy to generate and debug
3. **Human-Readable:** Can inspect with text editor or Excel
4. **Debugging:** Easy to verify correctness visually
5. **Pandas Support:** pandas.to_csv() is straightforward
6. **Universal:** Compatible with almost all systems
7. **Lightweight:** Small file size

**Why UTF-8 with BOM:**
- Handles Swedish characters (å, ä, ö) correctly
- BOM ensures Excel opens with correct encoding
- SmartSign properly interprets UTF-8

**Why NOT JSON:**
- More verbose for tabular data
- Less natural SmartSign integration
- Harder to inspect visually

**Why NOT XML:**
- Excessive verbosity
- Complex parsing
- Overkill for simple tabular data

**Why NOT direct database:**
- Security complexity
- Network firewall issues
- Overkill for 6-10 rows of data

### Consequences

**Positive:**
- Simple, proven format
- Easy troubleshooting
- Fast processing
- Small file sizes (< 5 KB typically)
- Easy to version control

**Negative:**
- Less structured than JSON/XML
- No built-in schema validation
- Commas in data require quoting

**Mitigation:**
- Pandas handles quoting automatically
- Data validation in Python script
- Column structure is stable and well-defined

---

## ADR-004: Weekly Filtering Strategy

### Context
Source Excel contains entire semester's seminars (175+ events spanning 3-4 months). Digital display should show only relevant seminars. Multiple filtering strategies possible: daily, weekly, bi-weekly, monthly, custom date range.

### Decision
**Filter to current week only (Monday 00:00 to Friday 23:59), excluding past events.**

### Rationale

**Why current week (Mon-Fri):**
1. **User Relevance:** Visitors care about "what's happening this week"
2. **Planning Window:** One week is optimal planning horizon
3. **Screen Real Estate:** 5-10 seminars fit well on display
4. **IML Schedule:** Seminars typically scheduled weekdays only
5. **Cognitive Load:** Too many seminars overwhelming; too few unhelpful
6. **Update Frequency:** Aligns with weekly planning cycles

**Why Monday-Friday:**
- Matches academic/business week
- IML seminars rarely on weekends
- Simplifies date logic

**Why exclude past events:**
- Past seminars are not actionable
- Prevents confusion
- Keeps display clean and current
- Automatic cleanup without manual intervention

### Consequences

**Positive:**
- Always relevant information
- Automatic cleanup of old data
- Manageable display size
- Clear user expectation (current week)
- No manual intervention needed

**Negative:**
- Weekend seminars not shown (rare but possible)
- Thursday visitors can't see next week
- Empty display if no seminars scheduled

**Mitigation:**
- Script shows clear message if no seminars found
- Could extend to "upcoming 7 days" in future version
- Weekly cycle matches user behavior patterns

### Alternatives Considered
1. **Next 7 days from today** - Rejected; creates inconsistent weekly boundaries
2. **Current + next week** - Rejected; too many items on screen
3. **Daily only** - Rejected; too narrow, not helpful for planning
4. **Full month** - Rejected; too many items, overwhelming

---

## ADR-005: Daily Batch Processing

### Context
Data updates could run on various schedules: real-time, hourly, daily, weekly, on-demand. Source Excel is updated manually and irregularly.

### Decision
**Run filtering script once per day at 00:00 (midnight) via scheduled task.**

### Rationale

**Why daily:**
1. **Source Update Frequency:** Excel updated manually, not in real-time
2. **Data Volatility:** Seminar schedules change infrequently
3. **Resource Efficiency:** Daily processing sufficient for use case
4. **Predictable Timing:** 00:00 ensures fresh data each morning
5. **Low Impact:** Off-hours processing doesn't interfere with other systems
6. **Simple Debugging:** Consistent daily schedule easy to monitor

**Why 00:00 (midnight):**
- After close of business
- Before staff/visitors arrive
- Aligns with daily boundary
- Low system load period

**Why NOT real-time:**
- Source data not real-time
- Unnecessary complexity
- Higher resource usage
- Monitoring overhead

**Why NOT hourly:**
- Overkill for infrequent data changes
- Unnecessary processing load
- No user benefit

**Why NOT weekly:**
- Risk of displaying outdated data
- Doesn't remove past seminars promptly
- Less responsive to schedule changes

### Consequences

**Positive:**
- Simple, predictable schedule
- Minimal resource usage
- Easy to monitor and debug
- Data fresh each morning
- Aligns with user expectations

**Negative:**
- Manual Excel updates take up to 24 hours to reflect
- No intraday updates if seminars change
- Midnight execution means no immediate feedback if errors occur

**Mitigation:**
- Excel rarely updated more than once per day
- Error logging captures issues
- Could add manual trigger for urgent updates
- Email notifications could be added for failures

### Alternatives Considered
1. **Hourly updates** - Rejected; unnecessary overhead
2. **Real-time triggers** - Rejected; source not real-time
3. **Weekly updates** - Rejected; past events not removed promptly
4. **Manual on-demand** - Rejected; defeats automation goal

---

## ADR-006: Windows Task Scheduler for Automation

### Context
Need to automate daily execution of Python script. Options: Windows Task Scheduler, cron (WSL), third-party scheduler, systemd service, custom daemon.

### Decision
**Use Windows Task Scheduler for script automation.**

### Rationale

**Why Windows Task Scheduler:**
1. **Native Solution:** Built into Windows, no installation needed
2. **Reliability:** Proven, battle-tested scheduling system
3. **GUI + CLI:** Easy configuration via GUI or schtasks.exe
4. **Logging:** Built-in execution logging
5. **Error Handling:** Configurable retry and error actions
6. **Wake Support:** Can wake computer if needed
7. **Security:** Runs with configured user permissions
8. **Familiar:** IT staff already know Task Scheduler

**Why NOT cron (WSL):**
- Requires WSL installation
- Less reliable on Windows
- More complex setup
- Unfamiliar to Windows admins

**Why NOT third-party scheduler:**
- Additional software dependency
- Licensing considerations
- Unnecessary complexity

**Why NOT custom daemon:**
- Significant development effort
- Maintenance burden
- Reinventing the wheel

### Consequences

**Positive:**
- Zero additional software needed
- Reliable execution
- Easy to configure
- Built-in logging
- Standard Windows administration
- Can manage via Group Policy if needed

**Negative:**
- Windows-specific (not portable to Linux)
- GUI interface sometimes unintuitive
- Requires admin privileges to configure

**Mitigation:**
- Document exact Task Scheduler configuration steps
- Provide schtasks.exe CLI command for automation
- Export task as XML for backup/version control

---

## ADR-007: Regex for Speaker Extraction

### Context
Speaker information embedded in HTML Description field in format: `<b>Speaker</b><br />\nName, Institution<br />`. Need to extract speaker name and institution. Options: HTML parser (BeautifulSoup), regex, string manipulation, ML-based extraction.

### Decision
**Use regular expressions (regex) for speaker extraction.**

### Rationale

**Why regex:**
1. **Pattern Consistency:** HTML format is consistent across all seminars
2. **Performance:** Regex is fast for simple patterns
3. **No Dependencies:** Built into Python standard library
4. **Sufficient Power:** Pattern is simple enough for regex
5. **Maintainability:** Single regex pattern easy to update
6. **Lightweight:** No external library needed

**Pattern used:**
```python
r'<b>Speaker</b><br\s*/?>[\n\s]*([^<]+?)(?:<br|$)'
```

**Why NOT BeautifulSoup:**
- Overkill for simple extraction
- Additional dependency
- Slower performance
- Not necessary for well-formed HTML

**Why NOT string manipulation:**
- Fragile to minor HTML variations
- More error-prone
- Less expressive

**Why NOT ML extraction:**
- Massive overkill
- Computational overhead
- Training data needed
- Unnecessary complexity

### Consequences

**Positive:**
- Fast execution
- No external dependencies
- Easy to understand and modify
- Handles minor HTML variations (self-closing tags)
- Captures name and institution together

**Negative:**
- Brittle if HTML format changes significantly
- Regex can be hard to read for non-experts
- May fail on malformed HTML

**Mitigation:**
- HTML format is controlled by seminar system (stable)
- Regex includes some flexibility (optional spaces, tag variations)
- Returns empty string gracefully if pattern doesn't match
- Could log warnings for failed extractions

### Alternatives Considered
1. **BeautifulSoup HTML parser** - Rejected; unnecessary dependency
2. **lxml parser** - Rejected; overkill
3. **String split/find methods** - Rejected; too fragile
4. **Machine learning** - Rejected; absurd complexity

---

## ADR-008: Tag-Based Content Filtering

### Context
Not all seminars should appear on public displays. Source system uses Tag(s) column with various tags. Need mechanism to selectively display seminars. Options: tag filtering, manual curation, separate export, all-or-nothing.

### Decision
**Filter seminars to include only those with "website" tag in Tag(s) column.**

### Rationale

**Why tag-based filtering:**
1. **Existing Mechanism:** Tag(s) column already exists in source data
2. **Programmatic Control:** Tag assignment happens in source system
3. **Flexibility:** Easy to add/remove tags in source system
4. **Scalability:** Works for hundreds of seminars
5. **Separation of Concerns:** Content selection separate from display logic
6. **No Manual Steps:** Automatic filtering based on tags
7. **Clear Semantics:** "website" tag clearly indicates public display intent

**Why "website" tag specifically:**
- Already in use by IML for public-facing content
- Consistent with existing workflows
- Clear semantic meaning
- Easy for program coordinators to understand

**Filtering logic:**
```python
df['Tag(s)'].str.contains('website', na=False)
```

**Why NOT manual curation:**
- Requires ongoing manual effort
- Error-prone
- Not scalable
- Defeats automation goal

**Why NOT separate export:**
- Requires source system changes
- More complex workflow
- Additional export to manage

**Why NOT all-or-nothing:**
- Some seminars are internal-only
- Need selective display
- Privacy/appropriateness concerns

### Consequences

**Positive:**
- Zero manual filtering effort
- Control remains in source system
- Clear ownership (program coordinators)
- Flexible and scalable
- Easy to understand rule
- Graceful handling of missing tags

**Negative:**
- Dependency on correct tagging in source system
- If tagging forgotten, seminar won't appear
- No validation that tags are correct

**Mitigation:**
- Document tagging requirement clearly
- Script logs number of filtered seminars (can spot anomalies)
- Could add email alerts if zero seminars found
- Training for program coordinators on tagging

### Alternatives Considered
1. **Display all seminars** - Rejected; some are internal-only
2. **Room-based filtering** - Rejected; room doesn't indicate public/private
3. **Manual whitelist** - Rejected; maintenance burden
4. **Date range filtering only** - Rejected; insufficient selectivity
5. **Multiple tags (AND/OR logic)** - Rejected; unnecessary complexity for MVP

---

## Summary of Key Architectural Principles

1. **Simplicity First:** Choose simple, proven solutions over complex alternatives
2. **Standard Technologies:** Leverage standard libraries and protocols (Python, CSV, HTTPS, Task Scheduler)
3. **Automation:** Minimize manual intervention at every step
4. **Separation of Concerns:** Keep data filtering separate from display logic
5. **Debuggability:** Human-readable formats, clear logging, easy inspection
6. **Maintainability:** Well-documented, standard tools, minimal dependencies
7. **Reliability:** Daily execution, graceful error handling, clear failure modes

---

## Technology Stack Summary

| Component | Technology | Justification |
|-----------|------------|---------------|
| Data Processing | Python 3.8+ with pandas | Industry standard for data manipulation |
| Data Format | CSV (UTF-8 with BOM) | Simple, universal, SmartSign native support |
| Distribution | HTTPS web server | Reliable, well-documented, accessible |
| Automation | Windows Task Scheduler | Native, reliable, familiar |
| Parsing | Regular expressions | Fast, no dependencies, sufficient for use case |
| Filtering | Tag-based (pandas) | Programmatic, flexible, automated |

---

## Decision Log

| ADR | Decision | Date | Status |
|-----|----------|------|--------|
| ADR-001 | Web-based CSV hosting | 2025-11-17 | Approved |
| ADR-002 | Python for processing | 2025-11-17 | Approved |
| ADR-003 | CSV data format | 2025-11-17 | Approved |
| ADR-004 | Weekly filtering | 2025-11-17 | Approved |
| ADR-005 | Daily batch processing | 2025-11-17 | Approved |
| ADR-006 | Windows Task Scheduler | 2025-11-17 | Approved |
| ADR-007 | Regex for speaker extraction | 2025-11-17 | Approved |
| ADR-008 | Tag-based filtering | 2025-11-17 | Approved |

---

## Future Considerations

As the system evolves, future ADRs may be needed for:

1. **Multi-language support** (Swedish/English)
2. **Email notification system** for errors
3. **API integration** with seminar management system
4. **Real-time updates** if source system becomes real-time
5. **Multi-screen support** with different filtering rules
6. **A/B testing** of display layouts
7. **Analytics** on seminar attendance correlation

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-17 | IML IT Team | Initial version with 8 ADRs |

---

**Approved by:** IML IT Team
**Date:** 2025-11-17
**Review Date:** 2026-11-17 (or when significant changes proposed)
