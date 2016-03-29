package models

import java.net.{InetAddress, InetSocketAddress}

import com.datastax.driver.core.Cluster
import com.typesafe.config.ConfigFactory
import com.websudos.phantom.connectors.SessionProvider
import com.websudos.phantom.connectors.{KeySpace, SessionProvider}
import com.websudos.phantom.dsl.Session

import scala.collection.JavaConversions._


/**
  * Created by michael on 1/16/16.
  */
trait CassandraConnector extends SessionProvider {

  val config = ConfigFactory.load()

  implicit val space: KeySpace = Connector.keyspace

  val cluster = Connector.cluster

  override implicit lazy val session: Session = Connector.session
}

object Connector {

  val config = ConfigFactory.load()
  val hosts = config.getStringList("cassandra.hosts")
  val ports = config.getIntList("cassandra.ports")

  val inets = hosts zip ports map (s => new InetSocketAddress(InetAddress.getByName(s._1), s._2))

  val keyspace: KeySpace = KeySpace(config.getString("cassandra.keyspace"))

  val cluster =
    Cluster.builder()
      .addContactPointsWithPorts(inets)
      .withCredentials(config.getString("cassandra.username"), config.getString("cassandra.password"))
      .build()

  val session: Session = cluster.connect(keyspace.name)
}
