import org.joda.time.DateTime
import java.util.UUID
import models.Curated

def uuidGen(s: String) = {
  java.util.UUID.nameUUIDFromBytes(s.toCharArray map (_.toByte))
}

val c = Curated(
  uuidGen("abc"),
  "human",
  "abc",
  new DateTime(),
  "mike",
  "tongji",
  "Nat"
)