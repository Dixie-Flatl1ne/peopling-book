\pset footer off
\echo === CORPUS ===
SELECT 'messages_total' AS metric, COUNT(*)::text AS value FROM raw.messages
UNION ALL SELECT 'wa_messages', COUNT(*)::text FROM raw.messages WHERE channel='whatsapp'
UNION ALL SELECT 'discord_messages', COUNT(*)::text FROM raw.messages WHERE channel='discord'
UNION ALL SELECT 'wa_chats', COUNT(DISTINCT chat_id)::text FROM raw.messages WHERE channel='whatsapp'
UNION ALL SELECT 'wa_distinct_senders', COUNT(DISTINCT sender_id)::text FROM raw.messages WHERE channel='whatsapp'
UNION ALL SELECT 'wa_distinct_sender_names', COUNT(DISTINCT sender_name)::text FROM raw.messages WHERE channel='whatsapp'
UNION ALL SELECT 'wa_earliest', MIN(ts)::date::text FROM raw.messages WHERE channel='whatsapp'
UNION ALL SELECT 'wa_latest', MAX(ts)::date::text FROM raw.messages WHERE channel='whatsapp';

\echo === READ THE ROOM: group vs dm ===
SELECT CASE WHEN chat_id LIKE '%@g.us' THEN 'group' ELSE 'dm' END AS kind,
       COUNT(DISTINCT chat_id) AS chats, COUNT(*) AS msgs
FROM raw.messages WHERE channel='whatsapp' GROUP BY 1 ORDER BY 3 DESC;

\echo === CONTEXT BRIDGE: people across chats ===
SELECT 'people_in_multiple_chats' AS metric, COUNT(*)::text AS value FROM (
  SELECT sender_id FROM raw.messages WHERE channel='whatsapp' AND sender_id IS NOT NULL
  GROUP BY sender_id HAVING COUNT(DISTINCT chat_id) > 1
) x;

\echo === FACTS TOTAL/STATUS ===
SELECT 'facts_total' AS metric, COUNT(*)::text AS value FROM curated.facts;
SELECT status, COUNT(*) AS n FROM curated.facts GROUP BY status ORDER BY n DESC;

\echo === FACTS BY TYPE ===
SELECT fact_type, COUNT(*) AS n FROM curated.facts GROUP BY fact_type ORDER BY n DESC;

\echo === ACCESS SCOPE DISTRIBUTION (governed bridge) ===
SELECT access_scope, COUNT(*) AS chats FROM reference.chats GROUP BY access_scope ORDER BY chats DESC;
\pset footer off
\echo === CORRECTIONS (recovery / peopling-adjust) ===
SELECT 'correction_facts' AS metric, COUNT(*)::text AS value FROM curated.facts WHERE fact_type='correction';
SELECT 'correction_facts_accepted', COUNT(*)::text FROM curated.facts WHERE fact_type='correction' AND status='accepted';

\echo === PEOPLING DEPTH: top people by fact volume (subject) ===
SELECT COALESCE(p.display_name,'(unknown)') AS person, COUNT(*) AS facts
FROM curated.facts f
LEFT JOIN curated.persons p ON p.id = f.subject_person_id
WHERE f.subject_person_id IS NOT NULL
GROUP BY 1 ORDER BY 2 DESC LIMIT 12;

\echo === PEOPLE WITH DISTILLED PROFILES (subjects with >=5 facts) ===
SELECT 'people_with_5plus_facts' AS metric, COUNT(*)::text AS value FROM (
  SELECT subject_person_id FROM curated.facts WHERE subject_person_id IS NOT NULL
  GROUP BY subject_person_id HAVING COUNT(*) >= 5
) x;

\echo === RELATIONSHIP FACTS (bridge: who connects to whom) ===
SELECT 'relationship_facts' AS metric, COUNT(*)::text AS value FROM curated.facts WHERE fact_type='relationship';
