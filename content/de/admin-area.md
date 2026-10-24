---
title: Adminbereich
description: Benutzer, Plattform-Einstellungen, SSO, Git und E-Mail zu Vorgang im laufenden Betrieb verwalten.
---

# Adminbereich

Im **Adminbereich** konfigurierst du den größten Teil von Hinata direkt in der
App. Die Einstellungen landen in MongoDB, **überschreiben die Umgebung** und
wirken **ohne Neustart**.

!!! info "Wer Zugriff hat"
    Nur Benutzer mit der Rolle **`ADMIN`**. Jeder Endpunkt unter
    `/api/v1/admin/**` ist auch serverseitig auf Admins beschränkt. Andere
    Benutzer sehen den Bereich nie, auch Organisationsadmins nicht.

!!! note "Admins betreiben die Plattform, nicht die Projekte"
    Die Rolle `ADMIN` gibt keinen Einblick in fremde Arbeit. Ein Admin sieht
    nur Projekte, Teams, Vorgänge, Boards, Seiten, Suchtreffer und
    Zeiteinträge, bei denen er selbst Mitglied ist. Arbeitszeit, Freigaben,
    Abwesenheiten, Feiertage, Zeit-Tags, Ausnahmen vom Sperrdatum und
    Abrechnung liegen nicht mehr hier, sondern auf der Seite
    [Organisation](/de/organization.html) bei den Organisationsadmins.

![Hinata-Adminbereich](/assets/img/shot-admin.png)
*Nutzer, Plattform-Einstellungen, SSO, Git und E-Mail zu Vorgang an einem Ort.*

## Wie die Laufzeitkonfiguration funktioniert

Zum Starten braucht der Server nur wenige Umgebungsvariablen: ein JWT-Secret, die
Datenbankverbindung und ein Mail-Relay. SSO-Anbieter, E-Mail-Ingest, OAuth-Apps
für Git und die Plattform-Einstellungen richtest du im Adminbereich ein. Sie liegen in
MongoDB. Dabei gilt:

- **DB überschreibt Env.** Umgebungswerte wie `hinata.app.*` sind nur
  *Standardwerte*. Was du im Adminbereich setzt, gewinnt.
- **Kein Neustart nötig.** Änderungen an Anbietern oder Flags wirken ab der
  nächsten Anfrage, ohne Redeploy oder Neustart des Containers.
- **Secrets sind nur schreibbar.** OAuth-Client-Secrets, Tokens und Passwörter
  kannst du **setzen**, die Admin-API gibt sie aber nie zurück. Gespeicherte
  Git-Tokens sind zusätzlich mit AES-GCM verschlüsselt.

## Die Bereiche

Der Adminbereich hat drei Gruppen:

- **Allgemein**, **Plattform**, **Sicherheit** und **Moderation**
- **Authentifizierung**, **E-Mail** und **Git-Integration**
- **Audit-Protokoll** und **Benutzer**

### Feiertage der Plattform

Unter **Allgemein** wählst du neben Zeitzone und Sprache die Region, deren gesetzliche Feiertage die Organisation bekommt, zum Beispiel Deutschland oder Bayern. **Automatisch** nimmt das Land der Zeitzone, **Keine** legt keinen Kalender an. Aus der Region macht der Server einen Feiertagskalender und füllt ihn jedes Jahr von selbst. Änderst du die Region, folgt ihr dieser Kalender. Was die Organisation daraus macht, entscheidet sie selbst, siehe [Feiertage](/de/organization.html#feiertage).

### Benutzer

Hier verwaltest du die Personen auf deiner Instanz:

- ausstehende Registrierungen **genehmigen**
- Konten **aktivieren** oder deaktivieren
- **Rollen** zuweisen: **Admin** (`ADMIN`), **Organisationsadmin**
  (`ORG_ADMIN`) und **Moderation** (`MODERATOR`). Die drei sind unabhängig
  voneinander, eine Person kann eine, mehrere oder keine haben. Mehrere
  Personen auf einmal machst du über die Auswahl zu Organisationsadmins oder
  nimmst ihnen die Rolle. Die Moderation vergibst du im Fenster der Person.
- die **Anmeldeadresse** einer Person ändern

Für die Rollen gelten ein paar Regeln. Dich selbst kannst du nicht zum
Organisationsadmin machen, das muss ein anderer Administrator tun. Das dient
der Nachvollziehbarkeit und ist keine harte Sperre: Mit einem zweiten
Administratorkonto ließe sich die Rolle trotzdem vergeben. Deshalb steht jede
Vergabe im Audit-Protokoll, das lässt sich nicht abschalten, und alle
Organisationsadmins werden benachrichtigt. Der letzte
Organisationsadmin lässt sich nicht entfernen, deaktivieren oder löschen. Kommt
jemand zur Rolle dazu oder gibt sie ab, bekommen alle Organisationsadmins eine
Benachrichtigung. Für die Moderation gilt dasselbe: nicht an dich selbst, die
letzte Person mit der Rolle bleibt, jede Vergabe steht im Audit-Protokoll, und
alle, die moderieren, erfahren davon.

Änderst du die Anmeldeadresse einer Person, bekommt sie an ihrer alten Adresse
eine Nachricht darüber. Einen Tag lang geht danach kein Zurücksetzen des
Passworts an sie, weder aus dem Adminbereich noch über die öffentliche Seite
„Passwort vergessen“. Dort wird in dieser Zeit ohne Rückmeldung einfach nichts
verschickt. So kann niemand über die neue Adresse
unbemerkt ein Konto übernehmen.

Nach dem Update auf eine Version mit Organisationsadmins ist jeder bisherige
Admin einmalig auch Organisationsadmin, damit nichts stehen bleibt. Das steht
für jede Person einzeln im Audit-Protokoll, und jede bekommt eine
Benachrichtigung. Willst du
die Rollen trennen, nimm sie hier bewusst auseinander. Siehe
[Organisation](/de/organization.html).

Mit dem Update auf eine Version mit Moderation ist außerdem jeder bisherige
Admin einmalig auch Moderator, damit Meldungen von Anfang an jemanden
erreichen. Auch das steht je Person im Audit-Protokoll. Die Benachrichtigung
empfiehlt, die Rolle an Personen zu geben, die nicht die Plattform betreiben.

Ist die Selbstregistrierung mit Admin-Genehmigung aktiv (siehe unten), warten neue
Anmeldungen hier, bis ein Admin sie freigibt.

### Plattform

Drei Karten: welche Clients dein Server annimmt, wie sich Menschen anmelden und
was diese Plattform anbietet.

- **Mindestversion** (`minVersion`): die
  [Versionssperre](/de/clients.html#versionssperre). Ältere Clients müssen
  updaten. Überschreibt `HINATA_APP_MIN_VERSION`.
- **URL der Datenschutzerklärung**: der Link in der App. Pflicht für Releases im
  App Store und bei Google Play sowie für die DSGVO. Überschreibt
  `HINATA_PRIVACY_POLICY_URL`.
- **Anmeldung**: lokale Anmeldung, Selbstregistrierung und Freigabe durch die
  Administration. Lässt die Selbstregistrierung Menschen ohne Freigabe herein,
  sagt ein Hinweis unter den Schaltern, was das bedeutet (siehe **Wer
  hereinkommt** unten).
- **Plattform-Verhalten**: mehrere Personen an einem Vorgang, Antworten per
  E-Mail und **Projektvorlagen** (Projekte kopieren, das Vorlagen-Kennzeichen
  und Fristen als Versatz zum Termin des Projekts). Aus lassen heißt: Projekte
  verhalten sich genau wie bisher. Dieser Schalter hat drei Stellungen, denn
  leer bedeutet, dass `HINATA_PROJECT_TEMPLATES_ENABLED` entscheidet. Siehe
  [Projektvorlagen](/de/project-templates.html). Ob Fristen in Kalendertagen
  oder Arbeitstagen zählen, legen Organisationsadmins fest.
- **Schichtplanung**: Events mit Schichten, in die sich Leute eintragen. Auch
  dieser Schalter hat drei Stellungen, leer heißt, dass `HINATA_SHIFTS_ENABLED`
  entscheidet. Die Schichtplanung braucht ein MongoDB Replica Set. Läuft der
  Server ohne, steht hier statt des Schalters der Hinweis **Braucht ein MongoDB
  Replica Set**. Siehe [Schichtplanung](/de/shifts.html).
- **Erweiterte Zeiterfassung**: Hier siehst du nur, ob sie an ist. Eingestellt
  wird sie auf der Seite [Organisation](/de/organization.html). Bist du auch
  Organisationsadmin, führt dich die Zeile dorthin. Alle Schalter und
  Richtlinien erklärt [Zeiterfassung verwalten](/de/admin-time-tracking.html).

!!! tip "Gewinnt gegen die Umgebung"
    Alles unter Plattform überschreibt die passende
    `hinata.app.*`-Umgebungsvariable. Umgebungswerte sind nur der Startpunkt
    einer neuen Instanz.

### Moderation

Lässt ein Weg Menschen herein, ohne dass jemand entscheidet, beginnt der
Abschnitt mit **Wer hereinkommt**: Selbstregistrierung ohne Freigabe oder ein
SSO-Anbieter, der beim ersten Anmelden aktive Konten anlegt. Wer so ein Konto
hat, liest organisationsweite Seiten und das Verzeichnis. Nach dem Digital
Services Act gelten diese Inhalte dann als öffentlich, und die Instanz hat die
Pflichten einer Online-Plattform. **Freigabe einschalten** schließt alle
genannten Wege und speichert. Beim Update auf diese Version und bei jeder neuen
Instanz schließt Hinata sie selbst und sagt allen Admins Bescheid. Wer einen
Weg wieder öffnet, bestätigt das beim Speichern ausdrücklich. Jede Änderung
steht im Audit-Log.

Kommen Anfragen über einen Proxy, dem der Server nicht vertraut, steht einen
Tag lang eine Warnung über den Karten: Dann zählt jeder Client als Adresse des
Proxys. Setz `HINATA_TRUSTED_PROXIES`, siehe
[Reverse Proxy & TLS](/de/reverse-proxy.html).

Danach sechs Karten:

- **Wer moderiert**: alle Personen mit der Rolle Moderation. Sie prüfen
  gemeldete Inhalte und entscheiden über sie, sehen nur, was gemeldet ist, und
  haben keinen Zugang zum Adminbereich. Moderiert nur eine Person, steht hier
  der Hinweis, dass zwei besser sind: So entscheidet niemand über eine Meldung
  gegen sich selbst.
- **Kontakt für Meldungen**: Betreiber, E-Mail-Adresse und Link zum Impressum.
  Darüber erreichen Menschen, wer die Instanz betreibt. Die App-Stores verlangen
  einen veröffentlichten Kontakt, der Digital Services Act eine Kontaktstelle
  (Art. 11 und 12). Ohne Anmeldung steht der Kontakt in `/api/v1/meta`. Fehlt
  die E-Mail-Adresse, zeigt die Karte eine Warnung. Eine Adresse in
  `HINATA_MODERATION_CONTACT_EMAIL` gilt, solange hier keine eingetragen ist.
- **Aufbewahrung und Zahlen**: ob erledigte Fälle, ihre Meldungen und die
  Quarantäne nach 6 oder 12 Monaten gelöscht werden, außer die Strafverfolgung
  wurde informiert. **Jahreszahlen … herunterladen** gibt die Jahreszahlen der
  Moderation im Muster der EU-Kommission, eine CSV-Datei je Teil in einem ZIP,
  für dieses Jahr oder ein früheres. Was in den Zahlen steht und was du vor dem
  Veröffentlichen ergänzt, steht unter
  [Moderation für Betreiber](/de/moderation-operators.html#jahreszahlen).
- **Hausregeln**: dem stimmen alle zu, bevor sie schreiben. **Standard** ist
  eingebaut, in neun Sprachen, und nennt euren Kontakt. **Eigener Text** nimmt
  Markdown, **Adresse** eine eigene Seite (https). Was du auch wählst, der
  Server hängt **So moderieren wir** an: wie man meldet, dass ein Mensch jede
  Meldung prüft, ob Texte geprüft werden, wie es weitergeht und wie lange
  aufbewahrt wird. Jede gespeicherte Änderung ergibt eine neue Fassung, die sich
  nie mehr ändert. So zeigt jede Zustimmung und jede Entscheidung auf den
  Wortlaut, der damals galt. Eine neue Fassung fragt niemanden erneut, **Alle
  neu zustimmen lassen** schon. Bis eine Person zustimmt, bekommt sie kein
  neues Zugriffstoken, und kein KI-Client bekommt ihre Zustimmung. Ohne Konto
  liest jeder die Regeln unter `/api/v1/public/rules`, jede frühere Fassung mit
  `?version=N`.
- **Automatische Textprüfung**: welche Texte der Server beim Speichern ablehnt
  und ob er unklare Fälle zur Moderation gibt. Mehr dazu gleich unten.
- **Dateitypen**: ein Schalter je Gruppe, nämlich Bilder, PDF,
  Office-Dokumente, Text und Tabellen, ZIP und Sprachnachrichten. Dateien
  einer abgeschalteten Gruppe kann niemand mehr anhängen, in Texte einfügen
  oder senden. Die Schalter schränken die sichere Liste des Servers
  nur ein. SVG oder Programme lassen sich hier nie erlauben. Avatare und das
  Logo sind ausgenommen. Mehr dazu unter [Objektspeicher](/de/storage.html).

Die automatische Textprüfung vergleicht Texte beim Speichern mit Wortlisten:
Vorgänge, Kommentare, Wissensseiten, Name, Position und Pronomen im Profil,
Benutzernamen und die Namen von KI-Clients. Das gilt auf jedem Weg, in der
App, über MCP, aus E-Mails und aus Git. Nichts davon verlässt den Server. Code,
Logs und technische Begriffe wie `kill -9` lösen nichts aus. Die Karte hat:

- **Klare Verstöße ablehnen**, eingeschaltet. Drohungen, Hetze und Ähnliches
  werden nicht gespeichert. Wer schreibt, sieht, welches Wort es war, und
  behält den Entwurf.
- **Unklare Fälle zur Moderation geben**, ausgeschaltet, auch nach dem Update.
  Eingeschaltet wird der Text gespeichert, und die Moderation bekommt eine
  Meldung ohne meldende Person, nur für neue Funde aus den mitgelieferten
  Listen. Damit prüft das System die Texte eurer Mitglieder selbst. Je nach
  Organisation braucht es vorher die Zustimmung der Interessenvertretung, in
  Deutschland nach § 87 Abs. 1 Nr. 6 BetrVG oder dem Personalvertretungsrecht,
  und eine Datenschutz-Folgenabschätzung nach Art. 35 DSGVO. Deshalb fragt der
  Server beim Einschalten noch einmal nach.
- **Eigene Begriffe** werden immer abgelehnt, in jeder Schreibweise. Sie geben
  nie etwas zur Moderation, sonst ließe sich jede Erwähnung eines Namens oder
  des Betriebsrats dorthin leiten.
- **Ausnahmen** sind Wörter, die bei euch harmlos sind, etwa Fachbegriffe.
  Inhalte, die Kinder gefährden, bleiben trotzdem gesperrt. Beide Listen
  nehmen bis zu 500 Begriffe mit je 60 Zeichen.
- **Text ausprobieren** zeigt, was der Server mit einem Text täte, mit den
  gespeicherten Einstellungen. Der Text wird weder gespeichert noch gezählt.

Mitgeliefert sind Listen für Deutsch und Englisch. Für andere Sprachen wirken
nur eure eigenen Begriffe. Bilder und Anhänge prüft die Textprüfung nicht,
dafür gibt es Meldungen. **So moderieren wir** nennt eure eigenen Begriffe und
ob unklare Fälle zur Moderation gehen. Jede Änderung an Schaltern und Listen
steht im Audit-Log. Eine abgelehnte E-Mail wird kein Vorgang und bekommt keine
Antwort. Ihre Verbindung unter **E-Mail** zählt, wie viele es waren.

Wie Moderierende Meldungen abarbeiten, steht unter
[Moderation](/de/moderation.html). Was der Digital Services Act von dir als
Betreiber verlangt und wie die Jahreszahlen funktionieren, steht unter
[Moderation für Betreiber](/de/moderation-operators.html).

### Authentifizierung & SSO

Hier legst du fest, wie sich Personen anmelden:

- **lokale Authentifizierung**, **Selbstregistrierung** und
  **Admin-Genehmigung** ein- oder ausschalten
- **SSO-Anbieter** registrieren: OpenID Connect, OAuth 2.0, SAML 2.0 und LDAP
  (Synology SSO, Keycloak, Authentik, Azure AD, Google, …)
- je Anbieter **Neue Konten brauchen eine Freigabe**: Das erste Anmelden wartet
  wie eine Registrierung. Oder du nennst **Erlaubte E-Mail-Domains**: Nur diese
  kommen gleich herein, alle anderen warten. Ohne beides lässt der Anbieter
  herein, wen er kennt, und ein Hinweis unter seinen Schaltern sagt das.

Anbieter werden in Mongo gespeichert und wirken sofort. Siehe
[Authentifizierung](/de/authentication.html) und [Single Sign-on](/de/sso.html).

### Git-Integration

Registriere **eine OAuth-App pro Anbieter** (GitHub, GitLab, Bitbucket), damit
Projekte ihre Repositories verbinden können. Du trägst ein:

- Client-ID und Secret
- die öffentliche Basis-URL der API für OAuth-Callback und Webhooks
- optional ein Secret zur Verschlüsselung der Tokens

Das richtest du einmal für die ganze Plattform ein. Einzelne Repos verbinden die
Projekte danach in ihren eigenen Einstellungen. Siehe
[Git-Integration](/de/git-integration.html).

### E-Mail (Mail-to-Ticket)

Richte den **IMAP-Abruf** ein, damit aus eingehenden E-Mails Vorgänge werden.
Auch das liegt in Mongo und wirkt ohne Neustart. Mails leiten kannst du nur in
Projekte, in denen du selbst Mitglied bist. Siehe
[E-Mail zu Vorgang](/de/email-to-ticket.html).

### Audit-Protokoll

Zeigt die Einträge der Plattform: Anmeldungen, Konten, Konfiguration und
Integrationen.

- Einträge zu Arbeitszeit, Stundenzetteln und Abwesenheiten, Krankmeldungen
  eingeschlossen, siehst du hier nicht. Sie stehen nur im Protokoll auf der
  Seite [Organisation](/de/organization.html). Welche davon aufgezeichnet
  werden, legen die Organisationsadmins fest. Du kannst diese Schalter nicht
  umlegen, und der Hauptschalter des Audit-Protokolls bringt sie nicht zum
  Schweigen.
- Einträge zu Vorgängen und Seiten erscheinen ohne ihre Details, also ohne
  Vorgangsschlüssel und ohne Seiten-IDs.
- Änderungen an den Rollen Admin und Organisationsadmin und jede Änderung einer
  Anmeldeadresse durch einen Administrator werden immer aufgezeichnet. Das
  lässt sich nicht abschalten.

## Wie es weitergeht

- [Single Sign-on](/de/sso.html): einen Identitätsanbieter verbinden.
- [Git-Integration](/de/git-integration.html): OAuth-Apps und Repos pro Projekt.
- [E-Mail zu Vorgang](/de/email-to-ticket.html): eingehende Mails in Vorgänge umwandeln.
- [Authentifizierung](/de/authentication.html): Konten, Registrierung und 2FA.
- [Organisation](/de/organization.html): Zeiterfassung, Abwesenheiten und Fristen für die ganze Organisation.
